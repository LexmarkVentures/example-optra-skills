# RKNN Inference Server

This skill demonstrates the **Python + C++ Unix-socket inference pattern** used
in production Optra Edge skills on the CX2000 device.

## Why this pattern?

The RKNN runtime C API has lower per-frame overhead than the Python
`rknn_toolkit_lite2` bindings. Keeping the RKNN context in a long-lived C++
process and communicating with Python over a Unix domain socket gives you
near-native inference performance while keeping skill logic in Python.

## Architecture

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Docker container                                                             │
│                                                                               │
│  ┌─────────────────────┐     Unix socket (raw bytes) ┌──────────────────────┐ │
│  │   run.py (Python)   │ ──────────────────────────► │inference-server (C++)│ │
│  │                     │                             │                      │ │
│  │  • USB camera input │ ◄────────────────────────── │  • loads yolox_s.rknn│ │
│  │  • pre/post process │    msgpack bounding boxes   │  • rknn_run()        │ │
│  │  • cv2.imshow       │                             │  • NMS postprocess   │ │
│  └─────────────────────┘                             └──────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Data flow per frame:**

1. Python resizes the camera frame to 640×640 and sends the raw RGB bytes
   over the Unix socket.
2. The C++ server runs RKNN inference and returns msgpack-encoded bounding
   boxes `{x1, y1, x2, y2, conf, cls}`.
3. Python scales the boxes back to the original camera resolution, draws them
   on the frame, and shows the result on the HDMI display.

## Model

The skill uses **YOLOX-S** compiled for RKNN (80 COCO classes). The compiled
model file `yolox_s.rknn` is included in this directory and is copied into the
image at build time.

The `librknnrt.so` (v2.2.0) bundled in `inference_server/lib/` is the Rockchip
RKNN runtime shared library required on RK3566-based Optra hardware.

Instructions on how to download and convert this model yourself can be found here: [rknn_model_zoo](https://github.com/airockchip/rknn_model_zoo).

More information on the CX2000 Optra Device and how to run models on the NPU can be found here: [CX2000 NPU](../../../docs/cx2000-npu.md)

# Setup

Before building, fetch the Rockchip-proprietary runtime files that cannot be
distributed in this repository (confidential Rockchip license):

```sh
cd examples/adv_examples/rknn_inference_server
./fetch_rknn_deps.sh
```

This downloads the following files from the
[`airockchip/rknn-toolkit2`](https://github.com/airockchip/rknn-toolkit2)
repository at the pinned release tag (`v2.2.0`) and places them at the paths
the `Dockerfile` expects:

| Destination | Source |
|---|---|
| `inference_server/include/rknn_api.h` | `rknpu2/runtime/Linux/librknn_api/include/` |
| `inference_server/include/rknn_custom_op.h` | `rknpu2/runtime/Linux/librknn_api/include/` |
| `inference_server/include/rknn_matmul_api.h` | `rknpu2/runtime/Linux/librknn_api/include/` |
| `inference_server/lib/librknnrt.so` | `rknpu2/runtime/Linux/librknn_api/aarch64/` |

The script skips files that already exist. Pass `--force` to re-download them:

```sh
./fetch_rknn_deps.sh --force
```

# How to build

```sh
docker buildx build --platform linux/arm64 -t <registry>/rknn-inference-server --push .
```

# Required Privileges
  * USB cameras
  * HDMI
