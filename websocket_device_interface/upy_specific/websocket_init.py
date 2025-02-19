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

from microdot import Microdot # type: ignore
from microdot.websocket import with_websocket

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequestList
from Websocket_Device_Framework.websocket_device_interface.request_transceiver import handle_receive
from Websocket_Device_Framework.websocket_device_interface.upy_specific.interface_handler import websocket_receive, websocket_send



async def handler():
    free_port = 80
    
    app = Microdot()
    
    @app.route('/')
    @with_websocket  # type: ignore
    async def echo(request, ws):
        while True:
            message = await ws.receive()
            print(message)
            await handle_receive(ws, message)
            
    app.run(port=free_port)
            
    # Start WebSocket server on the found port
#    async with websockets.serve(lambda websocket, path: websocket_receive(websocket, handle_receive), "localhost", free_port):
#        print(f"Server started on localhost:{free_port}")
#        await asyncio.get_running_loop().create_future()  # Run indefinitely
