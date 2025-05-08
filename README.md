# Example Optra Skills

This repository provides a collection of example skills that you can build and deploy on the Optra platform. The goal is to offer practical examples for developers to reference and to help them become familiar with the Optra platform.

All applications running on Optra devices are executed within Docker containers, which are pulled from a Docker repository. The Optra Portal is used to manage these containers and configure which devices should run them.

In the Optra Portal, these applications are referred to as **skills**. A skill defines the Docker container that a device should pull, as well as additional configuration options, such as environment variables, login credentials, inputs, outputs, and privileges. Once a skill is created, it can be added to one or more devices through a **workflow**. A workflow can be configured to pipe skill outputs to actions, such as making API calls, sending an email, or sending data to a charting tool for analysis.

---

## Building and Deploying Example Optra Skills

Each example skill includes a `Dockerfile`, a `README.md`, and some Python scripts. To deploy a running skill on a device, follow these three steps:

1. Build and push the Docker image
2. Create the skill in the Optra Portal
3. Add the skill and device to a workflow

---

### 1. Building the Docker Container

First, ensure Docker is installed on your build device. You can follow the installation instructions [here](http://docker.com/get-started/).

Each example skill directory includes a sample Docker build command. It typically looks like this:

  docker buildx build --platform linux/arm64 -t <registry>/<skill_name> --push .


Run this command from the root of the skill directory. It will build the image and push it to your repository. Afterward, you can verify the image with:

  docker image list


---

### 2. Creating the Skill in the Optra Portal

Once the Docker image is pushed, the next step is to create a new skill in the Optra Portal that points to the Docker image you just pushed.

- Navigate to the **Skills** tab in the Optra Portal
- Click **New Skill** in the top-right corner
- Choose **Docker Image** as the skill type
- Fill out the skill configuration (name, version, privileges, etc.)

The required configuration details will be documented in the example skill's `README.md`.

> **Optional:** To add extra troubleshooting tools, add the `wingman` volume mounted at `/wingman`. For more details on using Wingman, refer to the **Wingman** section under the "developer-notes."

---

### 3. Add a Device and Skill to a Workflow

To deploy a skill to a device, a **Workflow** must be created. Here’s how to do that:

1. Navigate to the **Workflows** tab in the Optra Portal
2. Click **New Workflow**
3. Name your workflow, and add your target device and skill

Once added, the device and skill will appear **green**, indicating that the workflow has been modified, but the changes have not yet been pushed to the device. To deploy the changes:

- Click **Sync** in the top-right corner of the workflow
- Wait for the device to download and start the skill

To monitor progress:

- Select the device in the workflow
- Go to the **Skills** tab to view the skills that have been added and their statuses
- Click **Logs** to view any output from the skill

The status of the skill will initially be **Unknown** until it has been fully downloaded and started. Once the skill starts, the status will change to **Running** or **Stopped**.

