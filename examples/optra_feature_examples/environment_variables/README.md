# Environment Variables
This is a simple skill to show how to use the Environment variables in the Optra platform. While environment variables can be set in the Dockerfile or other methods, the Optra platform provides a way to set environment variables at the skill level. This skill will print out the environment variable every 10 seconds. To see the environment variable, you can either go to the logs in the portal or use wingman to get the logs from the container.

If you wanted to override the value of this environment variable per device, you can navigate to the device's settings page and change the value of you environment variable.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/environment_variables --push .


# Environment Variables
  * Add an Environment Variable
    * Env Key = "EXAMPLE_ENV_VAR"
    * Env Value = "example"