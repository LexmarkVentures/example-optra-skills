# Outputs
This is a simple skill that shows how to use skill outputs. Outputs are a way to define data that you want to get from the skill and show it in the portal. The data is sent using Azure IoT messages; these messages are processed by the portal and then are used by "Actions" to do things like send emails or chart data.

For this example, the easiest action to configure is an email. Go to the workflow that has your skill running. Add a new action, select "Email Notification", then select the checkbox next to the name of your outputs example skill. Then fill in the information like this:

```
Recipients: <your_email>
Subject: "Output Example"
Message Template: "Counter: ${counter}"
```

*** In this message template, ${counter} will be replaced with the value of the counter output. ***

Once the workflow is synced, you will start to get emails with the counter value.


# How to build

```sh
docker buildx build --platform linux/arm64 -t <registry>/outputs --push .
```


# Outputs
  * Add an output
    * Output Key = "counter"
    * Output Label = "Counter"
    * Data Type = "Number"