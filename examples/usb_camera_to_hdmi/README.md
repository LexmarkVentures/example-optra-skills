# USB Camera to HDMI

This is a simple sample skill that uses opencv to grab frames from a usb camera and show them on a hdmi monitor.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/usb_camera_to_hdmi --push .


# Required Permissions
  * USB cameras
  * hdmi