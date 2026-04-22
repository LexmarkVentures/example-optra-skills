# Get RTSP (IP) Cameras Skill
This example shows how to obtain an IP-connected camera's URL from the Azure IoT Hub module twin.
While we often use a built-in camera finder to add cameras to a skill instead of adding them to the Cameras tab for each device in the Optra Portal, this example generally shows how to interface with the module twin and update the skill process based on changes happening in the module twin.
The async implementation will print out the connected cameras every time a camera is added or removed and the changes are synced to the workflow.

## How to Build

### Natively (ARM64):
```sh
docker build --platform linux/arm64 -t <registry>/get-rtsp-from-twin:<skill_tag> --push .
```

### Non-natively (x64):
```sh
docker buildx build --platform linux/arm64 -t <registry>/get-rtsp-from-twin:<skill_tag> --push .
```

## Required Privileges
No privileges required.

## Special Notes
Cameras must be added to the 'Cameras' tab of the device that is running the skill.

