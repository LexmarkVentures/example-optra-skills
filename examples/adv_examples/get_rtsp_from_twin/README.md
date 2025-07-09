# Get RTSP (IP) Cameras Skill
This example shows how to obtain IP-connected camera's URL from the Azure IoT Hub module twin.
While we often use a built-in camera finder to add cameras to a Skill instead of adding them to the Cameras tab for each device in the Optra Portal, this example generally shows how to interface with the module twin and also update/make changes to the skill process based on changes happening in the module twin.
The async implementation will print out the connected cameras every time a camera is added/removed and the changes are synced to the workflow.

# How to build
## Natively (ARM64):
docker build --platform linux/arm64 -t <registry>/get-rtsp-from-twin:<skill_tag> --push .

## Non-natively (x64):
docker buildx build --platform linux/arm64 -t <registry>/get-rtsp-from-twin:<skill_tag> --push .

# Required Privileges:
No privileges required.

# Special Notes:
Cameras must be added to the 'Cameras' tab of the device that is running the skill.

