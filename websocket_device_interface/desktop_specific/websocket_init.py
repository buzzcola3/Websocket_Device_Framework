import asyncio
import websockets.server
import socket

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequestList
from Websocket_Device_Framework.websocket_device_interface.request_transceiver import handle_receive
from Websocket_Device_Framework.websocket_device_interface.desktop_specific.interface_handler import websocket_receive


# Function to find the first available port starting from port 80
def find_free_port(starting_port=80, max_port=512):
    for port in range(starting_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                # Port is already in use, try the next one
                continue
    raise Exception(f"No free port found between {starting_port} and {max_port}")

async def handler():
    # Find the first free port starting from 80
    free_port = find_free_port()

    # Start WebSocket server on the found port
    async with websockets.serve(lambda websocket, path: websocket_receive(websocket, handle_receive), "localhost", free_port):
        print(f"Server started on localhost:{free_port}")
        await asyncio.get_running_loop().create_future()  # Run indefinitely