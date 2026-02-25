# CX2000 Video Demo

## Build
```sh
docker buildx build --platform linux/arm64 --push -t $registry/$repository:$tag .
```

## Skill configuration
Enable the following privileges when creating the skill.
* Sound
* HDMI
* CX2000 Video Acceleration
* Port bindings (optional, for debugging)
  * Host port: 2200
  * Protocol: tcp
  * Container port: 2200

Set the `VIDEO_FILE` environment variable to the absolute path of a video on the image to play the video at start up.

## Skill shell
The sample skill spins up sshd on port 2200 in the container for development. This can be used to quickly copy new videos or binaries into the container. To get access to this shell you must add the public side of your ssh key to the authorized_keys file and rebuild the image.

Playing videos from the shell
* Unset `VIDEO_FILE` so the container does not play a video at start up.
* ssh into the container
* Source `/app/app.env`
  * E.g.: `. /app/app.env`
  * This configures the shell environment to match the main process.
* A `playvideo` script is available that will invoke gst-launch in a loop.
  * E.g.: `playvideo /video/YourVideo.mp4`
