# Copyright 2025 Samuel Betak
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 
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