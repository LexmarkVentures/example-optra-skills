# Optra Settings

Demonstrates reading device settings from the Optra settings service using the `SETTINGS_SOCKET` Unix domain socket method. This skill pulls a few of the more common settings and prints them to the logs.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/optra_settings --push .
