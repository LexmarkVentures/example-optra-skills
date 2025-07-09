# Get Optimal USB Camera Settings
This example skill parses v4l2-ctl output to obtain information about all connected USB cameras.
v4l2-ctl returns structured information about each connected USB camera and this information can be parsed to find supported formats, framerates, and resolutions.
A single USB camera can support multiple image formats with different capabilities (YUYV with very high resolution at 5 FPS, MJPG with moderately high resolution at 15 FPS, etc...)
Given a minimum and maximum framerate, this skill will find the 'optimal' format in terms of the format that offers the highest resolution/framerate combo within the given framerate range.

# How to build
## Natively (ARM64):
docker build --platform linux/arm64 -t <registry>/get-rtsp-from-twin:<skill_tag> --push .

## Non-natively (x64):
docker buildx build --platform linux/arm64 -t <registry>/get-rtsp-from-twin:<skill_tag> --push .

# Required Privileges
  * USB cameras