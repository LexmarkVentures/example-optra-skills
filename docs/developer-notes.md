# Developer Notes

## Docker Images

All applications—referred to as "skills"—that run on Optra devices are packaged in Docker images. This creates a discrete, isolated, and scalable environment for your application. These Docker images operate with limited privileges, such as access to USB devices, exposed ports, and mounted volumes. Any privileges required by your skill must be explicitly specified when adding the skill via the portal.

## Common Development Cycle

If a device is already running a skill and a developer pushes a new image to the same Docker repository, the device will not automatically download the updated image. To force the device to pull the new version, use the **Resync** button in the workflow. This prompts the device to check whether the running container is up to date and to pull the new image if necessary. This enables rapid iteration and development on the Optra platform.

## Wingman

All Optra devices have a read-only filesystem, and SSH access is disabled. While this enhances security, it limits traditional development workflows common to Jetson devkits. To make development easier, we created a tool called **Wingman** for application development and testing.

Wingman is a restricted Bash shell that provides developers with access to the essential tools needed for Docker-based development. It can be installed from the skill marketplace. Once added to your organization, you can include the Wingman skill in any workflow. After the skill is running, navigate to its Web UI to launch the restricted shell on the device. Typing `help` in the shell will display a list of available commands.

Wingman enables developers to:

- View running skills on the device
- Inspect downloaded Docker images
- Use common development utilities similar to those available in an SSH session

To use Wingman to exec into a running container, you must add the **Wingman volume** under the skill's privileges. After this is configured, you can use the modified `docker-exec` command to enter the container as you would normally.
