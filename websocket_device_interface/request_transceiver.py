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

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequest, WsRequestList
import Websocket_Device_Framework.commands
from Websocket_Device_Framework.jsonrpc import JSONRPCResponseManager, dispatcher

try:
    import machine # type: ignore
    IS_MICROPYTHON = True
except:
    IS_MICROPYTHON = False

if IS_MICROPYTHON:
    from Websocket_Device_Framework.websocket_device_interface.upy_specific.interface_handler import websocket_receive, websocket_send
else:
    from Websocket_Device_Framework.websocket_device_interface.desktop_specific.interface_handler import websocket_receive, websocket_send

ws_request_list = WsRequestList(max_requests = 64)

async def handle_receive(ws, message):
    print("handleRX")
    if(message == "ping"):
        await handle_send(ws, "pong")
        return

    asyncio.create_task(handle_execute_and_send(ws, message))

async def handle_execute_and_send(ws, message):
    response = await JSONRPCResponseManager.handle(message, dispatcher)
    await handle_send(ws, response.json)
    pass

async def handle_send(ws, message):
    await websocket_send(ws, message)
