import asyncio
import websockets
import socket

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequestList
from Websocket_Device_Framework.websocket_device_interface.request_transceiver import handle_receive
from Websocket_Device_Framework.websocket_device_interface.request_transceiver import execute_and_send

ws_request_list = WsRequestList(max_requests=127)

async def wsHandler(ws):
    try:
        await handle_receive(ws, ws_request_list)
            
    except websockets.ConnectionClosedOK:
        print("Connection closed normally")
    except websockets.ConnectionClosedError:
        print("Connection closed with an error")
    except Exception as e:
        print(f"Error in handler: {e}")

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
    async with websockets.serve(wsHandler, "localhost", free_port):
        print(f"Server started on localhost:{free_port}")
        await asyncio.Future()  # Run indefinitely