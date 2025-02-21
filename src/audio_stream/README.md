# Audio Stream
This skill pulls audio from the microphone built into the Optra and records it to a
file. This file is saved to a volume on the device.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/audio_stream --push .


# Required Permissions
  * sound
  * Volumes
    * Volume Name: audioStreamExample
    * Mount Path: /app/outputs