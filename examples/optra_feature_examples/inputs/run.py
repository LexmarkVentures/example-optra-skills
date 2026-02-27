import time
from azure.iot.device import IoTHubModuleClient

def main():
    module_client = IoTHubModuleClient.create_from_edge_environment(
            websockets=True
        )
    print(f"Module Twin: {module_client.get_twin()}")

    while True:
        inputs = module_client.get_twin().get('desired', {}).get('inputs', {})
        print(f"Inputs: {inputs}")
        time.sleep(10)

if __name__ == '__main__':
    main()