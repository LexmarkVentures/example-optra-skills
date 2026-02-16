# Audio Stream
This skill pulls audio from the microphone built into the Optra device and prints the volume level to the terminal. To see the volume levels, you can either go to the logs in the portal or use wingman to get the logs from the container.

There are directions to comment or uncomment lines 40-45 depending on what device you are running on. There are some amixer commands that need to be ran to make sure that the microphone of the vz6100 devices are configured correctly and the name of the microphone device is slightly different on the two Optra models.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/audio_stream --push .


# Required Privileges
  * sound