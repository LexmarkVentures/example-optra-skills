# Example Optra Skills

Here is a collection of example skills that you can build and deploy on the Optra platform. The goal of this repo is to provide examples for developers to reference and to gain familiarity with the Optra platform.

All applications that run on an Optra device run in a docker container, these containers are pulled down from a docker repository. The Optra Portal is used to manage these containers and configure which devices should run them. In the Optra Portal, these applications are defined as skills. A skill defines the docker container the device should pull as well as other configuration that describes how a skill should be ran including environment variables, login credentials, inputs, output, and privileges. Once a skill has been created, it can be added to a device or list of devices using a workflow. A workflow can configured to to pipe skill outputs to actions which can make api calls, add data to a google sheet, or send data to the charting tool to be analyzed.

# Creating a Skill

  * cross buildx
  * adding skill to portal
  * all skill configuration:
    * inputs
    * outputs
    * environment vars
    * privileges


# Creating a workflow

  * add device and skill
  * configuring actions