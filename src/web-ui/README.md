# USB Camera to HDMI

This is a simple sample skill that creates a bare bones "Hello World" webui that is
accessible through the portal.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/webui --push .


# Required Permissions
  * webui -- port 3000