// Copyright (c) 2021 by Rockchip Electronics Co., Ltd. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//
// Modified by Lexmark
//

/*-------------------------------------------
                Includes
-------------------------------------------*/

#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <cstdlib>                  // for malloc and free
#include <msgpack.hpp>
#include <vector>
#include "postprocess.h"
#include "rk_common.h"
#include "rknn_api.h"

/*-------------------------------------------
                  Main Functions
-------------------------------------------*/
#define SOCKET_PATH "/tmp/inference_server.sock"

struct BBox {
    int x1, y1, x2, y2, cls;
    float conf;

    MSGPACK_DEFINE_MAP(x1, y1, x2, y2, conf, cls);
};

int main(int argc, char** argv)
{
    int            ret;
    //pipeline parameters
    if (argc < 4) {
        fprintf(stderr,"Usage: %s [model] [confidenceThreshold] [nmsThreshold] \n", argv[0]);
        return -1;
    }

    char*          model_path = argv[1];
    char*          box_conf_threshold_param = argv[2];
    float          box_conf_threshold = atof(box_conf_threshold_param);
    char*          nms_threshold_param = argv[3];
    float          nms_threshold = atof(nms_threshold_param);

    rknn_app_context_t rknn_app_ctx;
    memset(&rknn_app_ctx, 0, sizeof(rknn_app_context_t));

    rknn_context ctx = 0;

    // Create the neural network
    int            model_data_size = 0;
    unsigned char* model_data      = load_model(model_path, model_data_size);

    ret = rknn_init(&ctx, model_data, model_data_size, 0, NULL);
    //no need to hold the model in the buffer. Get some memory back
    free(model_data);

    if(ret < 0){
        printf("rknn_init fail! ret=%d\n", ret);
        return -1;
    }

    rknn_sdk_version version;
    ret = rknn_query(ctx, RKNN_QUERY_SDK_VERSION, &version, sizeof(rknn_sdk_version));
    if (ret < 0) {
        printf("rknn_init error ret=%d\n", ret);
        return -1;
    }

    // Get Model Input Output Number
    rknn_input_output_num io_num;
    ret = rknn_query(ctx, RKNN_QUERY_IN_OUT_NUM, &io_num, sizeof(io_num));
    if (ret != RKNN_SUCC)
    {
        printf("rknn_query fail! ret=%d\n", ret);
        return -1;
    }
    rknn_tensor_attr input_attrs[io_num.n_input];
    memset(input_attrs, 0, sizeof(input_attrs));
    for(uint32_t i = 0; i < io_num.n_input; i++) {
        input_attrs[i].index = i;
        ret                  = rknn_query(ctx, RKNN_QUERY_INPUT_ATTR, &(input_attrs[i]), sizeof(rknn_tensor_attr));
        if (ret < 0) {
            printf("rknn_init error ret=%d\n", ret);
            return -1;
        }
        //dump_tensor_attr(&(input_attrs[i]));
    }

    rknn_tensor_attr output_attrs[io_num.n_output];
    memset(output_attrs, 0, sizeof(output_attrs));
    for(uint32_t i = 0; i < io_num.n_output; i++) {
        output_attrs[i].index = i;
        ret                   = rknn_query(ctx, RKNN_QUERY_OUTPUT_ATTR, &(output_attrs[i]), sizeof(rknn_tensor_attr));
        //dump_tensor_attr(&(output_attrs[i]));
    }

    // Set to context
    rknn_app_ctx.rknn_ctx = ctx;

    // TODO
    if (output_attrs[0].qnt_type == RKNN_TENSOR_QNT_AFFINE_ASYMMETRIC && output_attrs[0].type != RKNN_TENSOR_FLOAT16)
    {
        rknn_app_ctx.is_quant = true;
    }
    else
    {
        rknn_app_ctx.is_quant = false;
    }

    rknn_app_ctx.io_num = io_num;
    rknn_app_ctx.input_attrs = (rknn_tensor_attr *)malloc(io_num.n_input * sizeof(rknn_tensor_attr));
    memcpy(rknn_app_ctx.input_attrs, input_attrs, io_num.n_input * sizeof(rknn_tensor_attr));
    rknn_app_ctx.output_attrs = (rknn_tensor_attr *)malloc(io_num.n_output * sizeof(rknn_tensor_attr));
    memcpy(rknn_app_ctx.output_attrs, output_attrs, io_num.n_output * sizeof(rknn_tensor_attr));

    if (input_attrs[0].fmt == RKNN_TENSOR_NCHW){
        rknn_app_ctx.model_channel = input_attrs[0].dims[1];
        rknn_app_ctx.model_height = input_attrs[0].dims[2];
        rknn_app_ctx.model_width = input_attrs[0].dims[3];
    }
    else{
        rknn_app_ctx.model_height = input_attrs[0].dims[1];
        rknn_app_ctx.model_width = input_attrs[0].dims[2];
        rknn_app_ctx.model_channel = input_attrs[0].dims[3];
    }

    if(ret != 0){
        printf("init_fail! ret=%d model_path=%s\n", ret, model_path);
        return ret;
    }

    // You may not need resize when src resolution equals to dst resolution
    rknn_input inputs[rknn_app_ctx.io_num.n_input];
    rknn_output outputs[rknn_app_ctx.io_num.n_output];

    int server_socket = socket(AF_UNIX, SOCK_STREAM, 0);
    if (server_socket < 0) {
        std::cerr << "Failed to create socket" << std::endl;
        return 1;
    }

    sockaddr_un addr;
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);
    unlink(SOCKET_PATH);

    if (bind(server_socket, (sockaddr*)&addr, sizeof(addr)) < 0) {
        std::cerr << "Failed to bind socket" << std::endl;
        return 1;
    }

    if (listen(server_socket, 5) < 0) {
        std::cerr << "Failed to listen on socket" << std::endl;
        return 1;
    }
	int client_socket = accept(server_socket, nullptr, nullptr);
    if (client_socket < 0) {
        std::cerr << "Failed to accept connection" << std::endl;
        return 1;
    }
    int person_index = 0;
    while(1){
        std::vector<u_char> buf(640 * 640 * 3);
	    size_t total_received = 0;
	    while (total_received < buf.size()) {
            int bytes_received = read(client_socket, buf.data() + total_received, buf.size() - total_received);
            if (bytes_received <= 0) {
                std::cerr << "Failed to read data from socket" << std::endl;
                return 1;
            }
	    total_received += bytes_received;
	    }
	    void* data = static_cast<void*>(buf.data());
        //declare your list
        object_detect_result_list od_results;

        // Set Input Data
        inputs[0].index = 0;
        inputs[0].type = RKNN_TENSOR_UINT8;
        inputs[0].fmt = RKNN_TENSOR_NHWC;
        inputs[0].size = rknn_app_ctx.model_width * rknn_app_ctx.model_height * rknn_app_ctx.model_channel;
        inputs[0].buf = data;

        // allocate inputs
        ret = rknn_inputs_set(rknn_app_ctx.rknn_ctx, rknn_app_ctx.io_num.n_input, inputs);
        if(ret < 0){
            printf("rknn_input_set fail! ret=%d\n", ret);
            return -1;
        }
        // allocate outputs
        memset(outputs, 0, sizeof(outputs));
        for(uint32_t i = 0; i < rknn_app_ctx.io_num.n_output; i++){
            outputs[i].index = i;
            outputs[i].want_float = (!rknn_app_ctx.is_quant);
        }
        // run
        rknn_run(rknn_app_ctx.rknn_ctx, nullptr);
        rknn_outputs_get(rknn_app_ctx.rknn_ctx, rknn_app_ctx.io_num.n_output, outputs, NULL);

        // post process
        float scale_w = 1.0;
        float scale_h = 1.0;

        post_process(&rknn_app_ctx, outputs, box_conf_threshold, nms_threshold, scale_w, scale_h, &od_results);

        std::vector<BBox> bounding_boxes;
        for (int i = 0; i < od_results.count; i++) {
            object_detect_result* det_result = &(od_results.results[i]);
	        int cls = det_result->cls_id;

            BBox bbox;
            bbox.x1 = det_result->box.left;
            bbox.y1 = det_result->box.top;
            bbox.x2 = det_result->box.right;
            bbox.y2 = det_result->box.bottom;
            bbox.conf = det_result->prop;
            bbox.cls = cls;
	        bounding_boxes.push_back(bbox);
        }
        std::map<std::string, std::vector<BBox>> detections;
	    detections["results"] = bounding_boxes;

        msgpack::sbuffer sbuf;
        msgpack::pack(sbuf, detections);
	    write(client_socket, sbuf.data(), sbuf.size());
        ret = rknn_outputs_release(ctx, io_num.n_output, outputs);
    }

    if(rknn_app_ctx.input_attrs  != NULL) free(rknn_app_ctx.input_attrs);
    if(rknn_app_ctx.output_attrs != NULL) free(rknn_app_ctx.output_attrs);
    if (rknn_app_ctx.rknn_ctx != 0) rknn_destroy(rknn_app_ctx.rknn_ctx);
    close(server_socket);

    return 0;
}
