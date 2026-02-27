# Inputs
This is a simple skill that shows how to use skill inputs. Inputs are a way to configure a skill from the portal. The configuration is sent to the device using azure iot hub device twin.

This skill will print the entire twin on start up and then print the inputs every 10 seconds. To see the inputs printed out, you can either go to the logs in the portal or use wingman to get the logs from the container.

Once the skill is running on the device, go to the workflows page and select the example skill in the workflow. If you configured the skill correctly, there will be a section called "inputs" and the input you configured should be listed with an input field. From here you can change this input field and once the workflow has been synced, you should see the input change in the logs. The input can be changed while the skill is running and the value will be changed without restarting the skill.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/inputs --push .


# Inputs
  * Add an input
    * Input Key = "example"
    * Input Label = "Example"