# Volumes
This is a simple skill that shows how to use volumes in a skill. Volumes allow a skill to save persistent data and configuration across device and skill restarts. This skill will print out a counter value every 10 seconds, incrementing each time, and saving the current counter value to the volume. To see the counter value, you can either go to the logs in the portal or use wingman to get the logs from the container.

Once the skill is running and the counter is incrementing, the skill can be restarted or the device power cycled. If the skill is configured correctly, the counter will start where it left off and continue incrementing.

# How to build

    docker buildx build --platform linux/arm64 -t <registry>/volumes --push .


# Required Privileges
  * Volumes
    * Volume Name = "VolumeExSkill"
    * Mount Path = "/app/volume_ex_skill"