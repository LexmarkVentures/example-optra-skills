# Skill Configuration

## What is a skill?

A skill is a docker containerized application that can be ran on Optra devices. This creates a discrete, isolated, and scalable environment for your application. These Docker images operate with limited privileges, such as access to USB devices, exposed ports, and mounted volumes. Any privileges required by your skill must be explicitly specified when adding the skill via the portal.

## Skill Configuration

When creating a skill, there are five main types of configuration: Container, Inputs, Outputs, Env, and Privileges. All of this configuration is defined in the Optra Portal.

### Container

This section configures all the basic docker repo information for the image used in the skill. A skill can use an image from a public repo or a private repo using a username and password. This section is also where the name, version, and appearance of the skill is configured.

### Inputs

Inputs are a way for a portal user to define configuration for all devices in a workflow. If a skill has an input, a user can click the skill in the workflow and change its value for all devices in that workflow. These inputs are sent to the device through the IoT twin and can be accessed in the skill using the Azure IoT device libraries (see inputs example skill). Inputs have two fields to configure: the key and the label. The key is the name of the field in the IoT message and the label is the human-readable description that will show in the portal.

### Outputs

Outputs are a way for a skill to send data to the portal. Like the inputs, this skill-portal communication is handled using azure iot messages (see outputs example skills). There is four fields to configure for the outputs: output key, output label, unhealthy after, and data type. Like the inputs the key is the name of the field from the iot message and the label is human readable name to be used in the portal. Unhealthy after is a metric that can be used to troubleshoot device connection and can be used to filter devices that have not sent an iot message for that length of time. The data type is simply the data type of the output. Lastly, there is an additional feature called "Enabled Status". This can be used to change the status of a device if an output is a certain value. 

### Env

The Env configuration is a way for environment variables to be configured from the portal. The configuration for this feature has two fields: key and value. The key is the name of the environment variable and value is its value.

> **Note:** Environment variables can also be set at the device level by clicking on the device in the workflow, navigating to the settings tab, and adding the variable in the env section.

## Privileges

Privileges define what the skill has access to when running on device. Privileges might include: usb cameras, mic and audio out, exposed ports, and hdmi. By default all this is turned off for security purposes.

All VZ devices have access to gpu by default. For more info on this see [Building GPU Enabled VZ Images](building-gpu-enabled-vz-images.md)

***For more information on how to use these configurations, refer to the examples directory for projects that use all these configurations***