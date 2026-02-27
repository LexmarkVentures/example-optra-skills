# Web UI

This is a simple sample skill that creates a bare bones "Hello World" webui that is accessible through the portal. After the skill is running, the webui can be accessed on the local network or by creating a tunnel through the portal.

The local address is "\<optra-ip>:\<port>/" where the port is not the same as the port configured in the privileges menu -- this is the port in the docker container. To get the external port, go to the portal and click on the skill in the workflow. From here you will see the randomly generate external port and configuration to expose it on the local network.

To tunnel into the skills webui through the portal, click on the device in the workflow, then navigate to the skills tab. If the example skill is configured correctly there should be a "WEB UI" button next to the example skill. From here you can click "OPEN WEB UI" which will open a new tab tunneled into the device.

The web page is a blank white page with "Hello, world!" at the top.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/webui --push .


# Required Privileges
  * webui -- port 3000