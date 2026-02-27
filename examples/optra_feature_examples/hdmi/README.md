# HDMI Display

This is a simple sample skill that demonstrates HDMI output by drawing a bouncing ball animation to the display. The skill uses X11 to create a window and render graphics directly to the HDMI output of the Optra device.

The animation displays a red bouncing ball that moves around the screen, bouncing off the edges. A frame counter is also displayed to show that the animation is running. This example is useful for understanding how to configure HDMI/display privileges for skills that need graphical output.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/hdmi_display --push .


# Required Privileges
  * HDMI (enables X11 display access)
