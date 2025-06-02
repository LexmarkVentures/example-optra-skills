# Pytorch
This skill pulls frames from a camera, feeds them to a mobilenetV2 model, decorates the
frames with the detections then shows the skill on the monitor. The docker container has
pytorch installed with CUDA support.

# Docker login

The docker image for this example skill is based on a docker image distributed by
nvidia. To get access to these images, you will have to follow the instructions
[here](https://docs.nvidia.com/ngc/gpu-cloud/ngc-private-registry-user-guide/index.html#getting-started).
Once you have created an account and logged into nvcr.io using the `docker login nvcr.io`
you should be ready to build the skill.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/pytorch --push .


# Required Permissions
  * USB cameras
  * hdmi