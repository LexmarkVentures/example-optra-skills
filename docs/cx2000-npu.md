# CX2000 NPU Development Guide

## What is the CX2000?

The Optra CX2000 is an edge AI device built on the **Rockchip RK3566** SoC. It is designed for vision and inference workloads at the edge and runs the same Docker/Azure IoT Edge skill framework as all other Optra devices.

### Hardware Capabilities

| Component | Specification |
|---|---|
| CPU | Quad-core ARM Cortex-A55 @ 1.8 GHz |
| GPU | ARM Mali-G52 |
| NPU | 0.8 TOPS (INT8 / INT16 / FP16 / BF16) |

The NPU is the primary accelerator for ML inference. It is accessed through the **Rockchip RKNN runtime** and supports models originally trained in TensorFlow, PyTorch, Caffe, or ONNX — after conversion to the `.rknn` format (see the section below).


## Model Conversion with RKNN Toolkit 2

Models must be converted to the `.rknn` format on a **developer PC** (x86-64) using the RKNN Toolkit 2 before they can run on the CX2000 NPU. The converted model file is then bundled into the skill's Docker image.

### Key Repositories

[rknn-toolkit2](https://github.com/airockchip/rknn-toolkit2) — PC-side Python package for converting and quantizing models, and for simulating inference without a device.

[rknpu2](https://github.com/airockchip/rknpu2) — The device-side C/C++ runtime (`librknnrt.so`) and Python Lite2 bindings used to run `.rknn` models on the device.

[rknn_model_zoo](https://github.com/airockchip/rknn_model_zoo) — A collection of pre-converted `.rknn` models and the scripts used to produce them. A good starting point for common architectures (YOLO variants, ResNet, MobileNet, etc.).

### Conversion Workflow

The general flow is:

1. **Train or obtain** a model in a supported framework (ONNX, PyTorch, TensorFlow, Caffe).
2. **Install rknn-toolkit2** on your development PC following the instructions in the repo.
3. **Convert** the model using the Python API:
   ```python
   from rknn.api import RKNN

   rknn = RKNN()
   rknn.config(target_platform='rk3566')
   rknn.load_onnx(model='your_model.onnx')
   rknn.build(do_quantization=True, dataset='calibration_dataset.txt')
   rknn.export_rknn('your_model.rknn')
   rknn.release()
   ```
4. **Copy** the `.rknn` file into your skill's Docker image at build time.

For full API documentation, quantization options, and per-framework conversion guides, refer to the [rknn-toolkit2 documentation](https://github.com/airockchip/rknn-toolkit2/tree/master/doc).

### Quantization

INT8 quantization (`do_quantization=True`) dramatically improves NPU throughput and is strongly recommended for production skills. It requires a small calibration dataset (a representative set of ~100 input images) that is passed to `rknn.build()`. Without quantization the model runs in floating-point mode on the NPU, which may be slower.

> **Important:** Always set `target_platform='rk3566'` when building models for the CX2000. Models compiled for a different Rockchip target will fail to load at runtime.


## Running Inference on the CX2000

### Recommended: C++ Inference Server Pattern

For production skills the recommended approach is to run inference in a **long-lived C++ process** that communicates with the Python skill logic over a **Unix domain socket**. This pattern avoids the per-frame overhead of the Python bindings and delivers near-native NPU throughput.

A complete, working implementation of this pattern is provided in the
[rknn_inference_server example skill](../examples/adv_examples/rknn_inference_server).
That example demonstrates:

- A C++ server that loads an `.rknn` model, accepts raw image frames over a Unix socket, runs `rknn_run()`, and returns bounding-box results encoded with [msgpack](https://msgpack.org/).
- A Python `run.py` that handles the camera, pre/post-processing, and skill logic, communicating with the C++ server via the socket.

This separation keeps inference in the fast C runtime while leaving the skill orchestration layer in Python.

### Python Option (`rknn_toolkit_lite2`)

A Python-native option exists through the `rknn_toolkit_lite2` package included in the [rknpu2](https://github.com/airockchip/rknpu2) repository. However, the Python bindings are **not officially packaged or supported** in the current Optra skill base images. If you are interested in using the Python Lite2 API rather than the C++ server pattern, please **reach out to the Optra team** for guidance on enabling it in your environment.
