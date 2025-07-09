# Audio Stream
This skill pulls audio from the microphone built into the Optra device and prints the volume level to the terminal. To see the volume levels, you can either go to the logs in the portal or use wingman to get the logs from the container.

If running on a VZ6100, you will need to uncomment line 58 which configures the internal microphone. All other devices can be ran without that setup.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/audio_stream --push .


# Required Privileges
  * sound