# CX2000 Video Demo

This skill demonstrates hardware-accelerated video playback on the CX2000 using GStreamer. It reads a video file path from the `VIDEO_FILE` environment variable and plays it on the HDMI display at startup. The skill also runs an SSH daemon on port 2200, which can be used for development and copying files into the container.

# How to Build

```sh
docker buildx build --platform linux/arm64 -t <registry>/gstreamer_video_cx2000 --push .
```


# Required Privileges
  * Sound
  * HDMI
  * CX2000 Video Acceleration
  * Port bindings (optional, for debugging)
    * Host port: 2200
    * Protocol: tcp
    * Container port: 2200

# Environment Variables
  * `VIDEO_FILE` — absolute path to a video file on the image to play at startup

# Skill Shell

The skill runs an SSH daemon on port 2200 for development access. To use it, add the public side of your SSH key to the `authorized_keys` file and rebuild the image.

Playing videos from the shell:
* Unset `VIDEO_FILE` so the container does not play a video at startup.
* SSH into the container.
* Source `/app/app.env` (e.g. `. /app/app.env`) to configure the shell environment to match the main process.
* Use the `playvideo` script to invoke gst-launch in a loop (e.g. `playvideo /video/YourVideo.mp4`).
