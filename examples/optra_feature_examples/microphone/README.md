# Audio Stream
This skill pulls audio from the microphone built into the Optra device and prints the volume level to the terminal. To see the volume levels, you can either go to the logs in the portal or use wingman to get the logs from the container.

There are directions to comment or uncomment lines 40-45 depending on which device you are targeting. There are some amixer commands that need to be run to make sure that the microphone of the VZ6100 devices is configured correctly, and the name of the microphone device is slightly different between the two Optra models.

# How to build

```sh
docker buildx build --platform linux/arm64 -t <registry>/audio_stream --push .
```


# Required Privileges
  * sound