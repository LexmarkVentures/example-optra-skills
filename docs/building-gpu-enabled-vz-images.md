# Building GPU enabled docker images for Optra Devices

## Nvidia Runtime

All skills on VZ devices will be ran with the "--runtime nvidia" flag. This gives the skill access to the GPU. More info on this flag can be found here: [Nvidia Runtime](https://developer.nvidia.com/container-runtime).

To access the runtime bindings the skill's Dockerfile needs to define two special environment variables:

```Dockerfile
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all
```

The official Nvidia base images already define these variables so if your skill is based on them you don't need to add these. More information of these environment variables and what they do can be found here: [Specialized Configurations with Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html)

## Understanding L4T and JetPack for NVIDIA Jetson Devices

When developing for any NVIDIA Jetson IoT devices including Optra devices powered by Nvidia, it’s essential to understand two software components: **L4T** and **JetPack SDK**. Unlike typical desktop or server development, **you do not manually install GPU drivers** for the Jetson hardware.
Instead, everything needed — the Linux kernel, device drivers, and low-level system libraries — is already bundled inside **L4T** and installed automatically when your base images include these components

## What is L4T (Linux for Tegra)?

**Linux for Tegra (L4T)** is a modified Ubuntu Linux distribution tailored specifically for Jetson hardware.
It includes:
- A Linux kernel customized for Jetson SoCs
- Hardware drivers (GPU, camera, etc.)
- Low-level libraries like CUDA for device operation

Essentially, L4T is the **operating system** that allows the Jetson hardware to boot and function correctly.

Learn more here:
🔗 [Linux for Tegra (L4T) Documentation](https://developer.nvidia.com/embedded/linux-tegra)

## What is JetPack SDK?

**JetPack** is the **full development kit** built on top of L4T.
It includes:
- CUDA and cuDNN (for GPU-accelerated computing and neural networks)
- TensorRT (for optimized AI inference)
- DeepStream SDK (for video and image analytics)
- Multimedia APIs, OpenCV, and other essential libraries
- Tools for development, debugging, and flashing devices

JetPack provides all the building blocks needed for developing AI, computer vision, and multimedia applications on Jetson devices.

Learn more here:
🔗 [JetPack SDK Documentation](https://developer.nvidia.com/embedded/jetpack)

## How They Relate

**JetPack** includes a specific version of **L4T**, along with additional libraries and tools.
When you install or flash JetPack onto a Jetson device, you are also installing the matched L4T version underneath.

For reference:
🔗 [JetPack and L4T Version Mapping](https://developer.nvidia.com/embedded/jetpack-archive)


---

## Available Base Images for Development

### Nvidia Official Images
Nvidia provides a range of images to support development on their edge devices. Those images can be found here: [NGC Image Catalog](https://catalog.ngc.nvidia.com/). All images that have gpu support are based on the base L4T image and add tools and functionality on top of that. When using NVIDIA's L4T-based images for Jetson, it's important to understand that they are layered. The L4T Base Image provides the minimal Ubuntu root filesystem along with the essential drivers for Jetson hardware. The L4T CUDA Image builds on top of the Base Image by adding CUDA libraries for GPU acceleration. Finally, the L4T JetPack Image includes everything from the CUDA Image, plus additional AI, vision, and multimedia libraries (like cuDNN, TensorRT, DeepStream, and OpenCV).

### Jetson Container Images
Another place to get L4T enabled jetson images -- as well as some inspiration -- is the [Jetson Container Images Repo](https://github.com/dusty-nv/jetson-containers/tree/master). This repo contains many projects that have been developed for the nvidia platform as well as links to the docker repo that contains the images the projects are based on.

It is important when choosing an image, you make sure that the image is built on L4T and is the right version. Below is a chart to show L4T and Jetpack versions on Optra devices:

| Firmware Version    | 1.7.9                   | 1.8.x                   | 1.9.x                   | 2.2.x                         |
|---------------------|--------------------------|--------------------------|--------------------------|-------------------------------|
| Optra models        | VZ1000, VZ5000           | VZ1000, VZ5000           | VZ1000, VZ5000           | VZ5000, VZ5100, VZ6100        |
| Jetson platforms    | Nano, AGX Xavier, Xavier NX | Nano, AGX Xavier, Xavier NX | Nano, AGX Xavier, Xavier NX | AGX Xavier, Xavier NX, AGX Orin, Orin NX |
| OS                  | L4T Ubuntu 18.04         | L4T Ubuntu 18.04         | L4T Ubuntu 18.04         | L4T Ubuntu 20.04              |
| JetPack release     | 4.5.1                    | 4.6.1                    | 4.6.1                    | 5.1 / 5.1.2                   |
| L4T release         | 32.5.1                   | 32.7.1                   | 32.7.3                   | 35.2.1 / 35.4.1               |
| CUDA release        | CUDA 10.2                | CUDA 10.2                | CUDA 10.2.300            | CUDA 11.4 / 11.4.19           |

