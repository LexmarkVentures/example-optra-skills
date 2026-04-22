# USB Camera

This is a simple sample skill that uses opencv to grab frames from a usb camera and prints them in the terminal using ASCII characters. To run the example, you will need to plug in a usb camera to any of the usb inputs. To see the ASCII image, you can either go to the logs in the portal or use wingman to get the logs from the container.

# How to build

```sh
docker buildx build --platform linux/arm64 -t <registry>/usb_camera --push .
```


# Required Privileges
  * USB cameras