'''
This script shows an asynchronous way of polling the IoT Hub to obtain the RTSP streams of all connected IP cameras.
Using this example, you can run an application while also polling the IoT Hub for changes.
This specific example looks for cameras that are added in the 'Cameras' tab on the Optra Portal.
Most Optra Edge skills now include their own camera finder, which will not require cameras to be added in the Portal.
However, the module twin contains other information that might also be useful to asynchronously change.
'''
from azure.iot.device import IoTHubModuleClient

import asyncio
import logging

logger = None
command_queue = asyncio.Queue()

async def wait_process(process):
    await process.wait()

async def send_command(command):
    await command_queue.put(command)

async def get_command():
    return await command_queue.get()

async def setup():

    global module_client
    global current_uri

    """
    Create the IoT Hub Module Client to allow us to get the twin:
    """
    module_client = IoTHubModuleClient.create_from_edge_environment(
        websockets=True)
    logger.error("Created module_client")
    logger.error("Getting intial cameras...")
    current_uri = get_camera_uri(module_client)

    module_client.on_twin_desired_properties_patch_received = twin_changed

def twin_changed(data):
    logger.error("\nModule Twin changed.")
    try:
        sensors = data['device']['sensors']
        sensor_list = list(sensors)
        for i in range(0, len(sensor_list)):
            logger.error("Found camera URI: %s", sensors[sensor_list[i]]['ip'])
        logger.error("\n")

        # Use this command to restart the skill application if needed:
        command = "restart"
        asyncio.run_coroutine_threadsafe(send_command(command), loop)

    except Exception as e:
        logger.error(f"Exception {e}")

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

async def start_process():
    global current_uri
    args = ['python3', './run_forever.py']
    process = await asyncio.create_subprocess_exec(*args)
    return process

async def run():
    await setup()

    process = None

    while (True):

        if not process:
            logger.error("\nStarting process...")
            process = await start_process()

        if process:
            wait_for_process = asyncio.ensure_future(wait_process(process))
            wait_for_command = asyncio.ensure_future(get_command())

            done, pending = await asyncio.wait([wait_for_command, wait_for_process], return_when=asyncio.FIRST_COMPLETED)
            first = done.pop()
            if first == wait_for_command:
                result = first.result()
                print(f"Command received {result}")
                if result == "restart":
                    print(f"Restarting app")
                    process.terminate()
                    print(f"Waiting for process to terminate..")
                    await process.wait()
                    process = None


def main():
    global loop
    global logger

    logger = logging.getLogger('logger')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

if __name__ == '__main__':
    main()