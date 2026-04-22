# GPIO

This is a simple sample skill that demonstrates use of the GPIO pins on the VZ6100 and VZ5100 devices. This skill repeatedly loops through all the pins, turning them high then low. For more information about this feature, see the [GPIO Docs](../../../docs/gpio.md).

# How to build

```sh
docker buildx build --platform linux/arm64 -t <registry>/gpio --push .
```

# Required Privileges
  * GPIOS (enables GPIO pin access)
