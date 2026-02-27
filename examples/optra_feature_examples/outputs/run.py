import time
import json
from azure.iot.device import IoTHubModuleClient, Message

def main():
    module_client = IoTHubModuleClient.create_from_edge_environment(
            websockets=True
        )

    counter = 0
    while True:
        message = Message(
            json.dumps(
                {"data": {"counter": counter}}
            )
        ) # the portal requires a JSON object with a "data" key

        print(f"Sending message")
        module_client.send_message(message)
        counter += 1
        time.sleep(30)

if __name__ == '__main__':
    main()