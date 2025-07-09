'''
An example that gets the RTSP stream of each attached camera only ONCE.
This example will print the available cameras at the time of skill startup and will do nothing more.
'''
from azure.iot.device import IoTHubModuleClient

import logging

logger = None

def get_camera_uri(client):
    twin = client.get_twin()

    sensors = twin['desired']['device']['sensors']

    # If no cameras found, nothing we can do
    if len(sensors) == 0:
        return None
    
    sensor_list = list(sensors)

    for i in range(0, len(sensor_list)):
        logger.error("Found camera URI: %s", sensors[sensor_list[i]]['ip'])
    logger.error("\n")

def setup():

    global module_client
    global current_uri

    """
    The main application entry point.
    """
    module_client = IoTHubModuleClient.create_from_edge_environment(
        websockets=True)
    logger.error("Created module_client")
    logger.error("Getting intial cameras...")
    current_uri = get_camera_uri(module_client)

def main():
    global logger

    logger = logging.getLogger('logger')

    setup()



if __name__ == '__main__':
    main()