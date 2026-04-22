# Developer Notes

## Wingman

All Optra devices have a read-only filesystem, and SSH access is disabled. While this enhances security, it limits traditional development workflows common to Jetson devkits and other systems running Ubuntu. To make development easier, we created a tool called **Wingman** for application development and testing.

Wingman is a restricted Bash shell that provides developers with access to the essential tools needed for Docker-based development. It can be found in the skill marketplace. Once added to your organization, you can include the Wingman skill in any workflow. After the skill is running, navigate to its Web UI to launch the restricted shell on the device. Typing `help` in the shell will display a list of available commands.

Wingman enables developers to:

- View running skills on the device
- Inspect downloaded Docker images
- Use common development utilities similar to those available in an SSH session

### Exec into running docker image

Due to security, `docker exec ` has been removed but an alternative route has been provided. To use Wingman to exec into a running container, you must add the **Wingman volume** under the skill's privileges. After this is configured, you can use the modified `docker-exec <container-id>` command to enter the container as you would normally.

### Journal Logs

Sometimes it is not obvious what the status of a skill is from looking at the portal. A good way to get the raw logs from the Azure IoT process is to use Wingman to open a terminal on the device and run the `journalctl` command. This will give you all the raw logs from the device. These messages will have information about pulling images, starting containers, and IoT messages.

## SSH Daemon in a Running Container

An alternative to Wingman is to start an SSH daemon in the running Docker container. This allows a developer to directly access a running container for development, or use `scp` to copy data in or out of the container, without going through Wingman. An example of this can be found in the [gstreamer_video_cx2000 example](examples/adv_examples/gstreamer_video_cx2000).

## Azure IoT Device Management

The service running the Docker image on the device is [Azure IoT Edge](https://learn.microsoft.com/en-us/azure/iot-edge/about-iot-edge). Every Optra device has two Docker containers that always run: the azureiotedge-hub and the azureiotedge-agent. Using wingman to run `docker ps` you should see these containers running. These docker containers have access to the docker socket and manage all the skills on the device.

When a user syncs a workflow, a digital twin is updated in the cloud. This twin contains all information on what containers to run and how to run them. Azure IoT then sends that twin to the device. Once the device receives that twin, it must pull the images and start the containers. This process can be monitored using the journal described above.

## Common Development Cycles

### Override and Reload

If a device is already running a skill and a developer pushes a new image to the same url, you can force the skill to restart and pull the new image with the `reload <container_id>` command in wingman. This command will tail the logs of the existing container while it shuts down, attempt to pull the docker image, start the container again, and finally tail the logs of the new container. This prevents a user from having to create a new version of the skill in the portal and iterate quickly on the device.

### Develop in Running Container

Another common development cycle is to create a Docker image that never stops running and use `docker-exec` to develop and troubleshoot in a running container. For example, if a user had a skill that kept erroring, they could put this at the end of their Dockerfile:

```dockerfile
CMD ["tail", "-f", "/dev/null"]
```
which, when run, will never stop. This allows the user to use Wingman or an SSH daemon in the container to develop in a terminal using a text editor like vim or nano. This isn't always the most convenient development cycle but can help in a pinch.