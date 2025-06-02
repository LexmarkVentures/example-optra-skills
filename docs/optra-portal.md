# Optra Portal Tutorial

Here is a simple walkthrough to show a new user the Optra portal and get your first skill running on your device.

**To participate in this walk through, you will need an Optra device**

### Creating an Account

Navigate [Here](https://portal.optra.com/) to create an Optra account.

Once you have created an account, you should be redirected to the Workflows page in your own personal organization. You can see the details about your account by clicking on your name in the top right corner. From here you can see what organizations you are in as well as your credits and other details. At the top of the screen you will see some tabs: Workflows, Devices, Skills, and Users. Below, I will go into each of these tabs and describe what they do.

### Devices

The devices tab is used to enroll and search your devices. If you have a device, you can enroll it by clicking the "+ Enroll Device" button in the top right corner. Before enrolling, make sure the device is on the network; this can be done by connecting ethernet or logging into wifi. Wifi instructions can be found here: [Control Panel](control-panel.md).

Once the device is enrolled, you should see the device listed in this tab and you can click on the device to get more info about its network status, logs, and skills.

### Skills

The skills tab is used to create new skills, configure existing skills, and browse public skills in the marketplace. A skill is a containerized application that can be deployed on an Optra device.

To create your first skill in the Portal; select "+ New Skill" in the top right corner then select the "Docker Image" create skill option. From here you will see a menu to configure everything about the skill. There are five tabs: Container, Inputs, Outputs, Env, and Privileges.

For this walkthrough we will only be using the Container tab. For more information about these different configuration options or a deeper dive into skills go here:  [Skill Configuration](skills.md).

Now give the skill a simple name like "My First Skill" the type "docker.io/fluent/fluent-bit" into the "Docker Container URL" field. This is a simple open source utility for printing telemetry to standard out; if you are interested, the docs can be found here: [Fluent-bit](https://github.com/fluent/fluent-bit). Finally, click save at the bottom of the configuration page and you should see your skill listed under the skills tab.

### Workflows

A workflow is how a user deploys skills to the Optra devices. To create a new workflow, select "+ New Workflow" in the top right corner and give it a name. Then you should see your empty workflow listed. Now you can add your recently enrolled device and skill by selecting the "+ Add" button under the devices and skills section.

Once your device and skill has been added the "Sync" button should appear green in the top right corner of the workflow. When the button is green, this means that there are staged changes that you have made to the workflow that have not been pushed to the device. Now you can click that sync button to push the changes to the device.

It will take a while for the device to receive the new configuration from the portal, pull the docker image that you configured, and start the skill. You can monitor the state of the skill by selecting the device in the workflow, then navigating to the skills section. This will give you a list of all the skills that have been added to the device and their status. The status will either be: "Running", "Stopped", or "Unknown". While the docker image is being pulled, the status of the skill will be "Unknown" and should change to "Running" once started.

From here you can see the output of the example Fluent-Bit skill by going to the logs tab and selecting your skill from the dropdown in the top right corner. The output should look something like this:
```
Fluent Bit v4.0.3
* Copyright (C) 2015-2025 The Fluent Bit Authors
* Fluent Bit is a CNCF sub-project under the umbrella of Fluentd
* https://fluentbit.io

______ _                  _    ______ _ _             ___  _____ 
|  ___| |                | |   | ___ (_) |           /   ||  _  |
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   __/ /| || |/' |
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / / /_| ||  /| |
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V /\___  |\ |_/ /
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/     |_(_)___/ 


[2025/06/02 15:13:10] [ info] [fluent bit] version=4.0.3, commit=f5f5f3c17d, pid=1
[2025/06/02 15:13:10] [ info] [storage] ver=1.5.3, type=memory, sync=normal, checksum=off, max_chunks_up=128
[2025/06/02 15:13:10] [ info] [simd    ] disabled
[2025/06/02 15:13:10] [ info] [cmetrics] version=1.0.3
[2025/06/02 15:13:10] [ info] [ctraces ] version=0.6.6
[2025/06/02 15:13:10] [ info] [input:cpu:cpu.0] initializing
[2025/06/02 15:13:10] [ info] [input:cpu:cpu.0] storage_strategy='memory' (memory only)
[2025/06/02 15:13:10] [ info] [sp] stream processor started
[2025/06/02 15:13:10] [ info] [engine] Shutdown Grace Period=5, Shutdown Input Grace Period=2
[2025/06/02 15:13:10] [ info] [output:stdout:stdout.0] worker #0 started
[0] cpu.local: [[1748877191.842229649, {}], {"cpu_p"=>0.250000, "user_p"=>0.250000, "system_p"=>0.000000, "cpu0.p_cpu"=>0.000000, "cpu0.p_user"=>0.000000, "cpu0.p_system"=>0.000000, "cpu1.p_cpu"=>1.000000, "cpu1.p_user"=>1.000000, "cpu1.p_system"=>0.000000, "cpu2.p_cpu"=>0.000000, "cpu2.p_user"=>0.000000, "cpu2.p_system"=>0.000000, "cpu3.p_cpu"=>1.000000, "cpu3.p_user"=>1.000000, "cpu3.p_system"=>0.000000, "cpu4.p_cpu"=>0.000000, "cpu4.p_user"=>0.000000, "cpu4.p_system"=>0.000000, "cpu5.p_cpu"=>0.000000, "cpu5.p_user"=>0.000000, "cpu5.p_system"=>0.000000, "cpu6.p_cpu"=>0.000000, "cpu6.p_user"=>0.000000, "cpu6.p_system"=>0.000000, "cpu7.p_cpu"=>0.000000, "cpu7.p_user"=>0.000000, "cpu7.p_system"=>0.000000}]
[0] cpu.local: [[1748877192.841971856, {}], {"cpu_p"=>0.250000, "user_p"=>0.250000, "system_p"=>0.000000, "cpu0.p_cpu"=>0.000000, "cpu0.p_user"=>0.000000, "cpu0.p_system"=>0.000000, "cpu1.p_cpu"=>0.000000, "cpu1.p_user"=>0.000000, "cpu1.p_system"=>0.000000, "cpu2.p_cpu"=>0.000000, "cpu2.p_user"=>0.000000, "cpu2.p_system"=>0.000000, "cpu3.p_cpu"=>0.000000, "cpu3.p_user"=>0.000000, "cpu3.p_system"=>0.000000, "cpu4.p_cpu"=>1.000000, "cpu4.p_user"=>1.000000, "cpu4.p_system"=>0.000000, "cpu5.p_cpu"=>0.000000, "cpu5.p_user"=>0.000000, "cpu5.p_system"=>0.000000, "cpu6.p_cpu"=>0.000000, "cpu6.p_user"=>0.000000, "cpu6.p_system"=>0.000000, "cpu7.p_cpu"=>1.000000, "cpu7.p_user"=>1.000000, "cpu7.p_system"=>0.000000}]
[0] cpu.local: [[1748877193.842025055, {}], {"cpu_p"=>0.000000, "user_p"=>0.000000, "system_p"=>0.000000, "cpu0.p_cpu"=>0.000000, "cpu0.p_user"=>0.000000, "cpu0.p_system"=>0.000000, "cpu1.p_cpu"=>0.000000, "cpu1.p_user"=>0.000000, "cpu1.p_system"=>0.000000, "cpu2.p_cpu"=>0.000000, "cpu2.p_user"=>0.000000, "cpu2.p_system"=>0.000000, "cpu3.p_cpu"=>0.000000, "cpu3.p_user"=>0.000000, "cpu3.p_system"=>0.000000, "cpu4.p_cpu"=>0.000000, "cpu4.p_user"=>0.000000, "cpu4.p_system"=>0.000000, "cpu5.p_cpu"=>0.000000, "cpu5.p_user"=>0.000000, "cpu5.p_system"=>0.000000, "cpu6.p_cpu"=>0.000000, "cpu6.p_user"=>0.000000, "cpu6.p_system"=>0.000000, "cpu7.p_cpu"=>0.000000, "cpu7.p_user"=>0.000000, "cpu7.p_system"=>0.000000}]
[0] cpu.local: [[1748877194.842206910, {}], {"cpu_p"=>0.500000, "user_p"=>0.250000, "system_p"=>0.250000, "cpu0.p_cpu"=>2.000000, "cpu0.p_user"=>1.000000, "cpu0.p_system"=>1.000000, "cpu1.p_cpu"=>0.000000, "cpu1.p_user"=>0.000000, "cpu1.p_system"=>0.000000, "cpu2.p_cpu"=>1.000000, "cpu2.p_user"=>0.000000, "cpu2.p_system"=>1.000000, "cpu3.p_cpu"=>2.000000, "cpu3.p_user"=>1.000000, "cpu3.p_system"=>1.000000, "cpu4.p_cpu"=>0.000000, "cpu4.p_user"=>0.000000, "cpu4.p_system"=>0.000000, "cpu5.p_cpu"=>0.000000, "cpu5.p_user"=>0.000000, "cpu5.p_system"=>0.000000, "cpu6.p_cpu"=>0.000000, "cpu6.p_user"=>0.000000, "cpu6.p_system"=>0.000000, "cpu7.p_cpu"=>0.000000, "cpu7.p_user"=>0.000000, "cpu7.p_system"=>0.000000}]
[0] cpu.local: [[1748877195.842214988, {}], {"cpu_p"=>0.625000, "user_p"=>0.500000, "system_p"=>0.125000, "cpu0.p_cpu"=>0.000000, "cpu0.p_user"=>0.000000, "cpu0.p_system"=>0.000000, "cpu1.p_cpu"=>0.000000, "cpu1.p_user"=>0.000000, "cpu1.p_system"=>0.000000, "cpu2.p_cpu"=>0.000000, "cpu2.p_user"=>0.000000, "cpu2.p_system"=>0.000000, "cpu3.p_cpu"=>0.000000, "cpu3.p_user"=>0.000000, "cpu3.p_system"=>0.000000, "cpu4.p_cpu"=>1.000000, "cpu4.p_user"=>0.000000, "cpu4.p_system"=>1.000000, "cpu5.p_cpu"=>1.000000, "cpu5.p_user"=>1.000000, "cpu5.p_system"=>0.000000, "cpu6.p_cpu"=>1.000000, "cpu6.p_user"=>1.000000, "cpu6.p_system"=>0.000000, "cpu7.p_cpu"=>1.000000, "cpu7.p_user"=>0.000000, "cpu7.p_system"=>1.000000}]
```

## Conclusion

Now that you have created your own skill in the Optra portal, you should be ready to build your own docker image and custom skill. To do this, you can build your own or try one of the example skills in the src directory. 