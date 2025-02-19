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

import websockets

async def websocket_receive(ws, onReceiveCallback):
    """
    Listens to the WebSocket and calls callback funcion on every new message
    """
    try:
        # Continuously listen for messages from the WebSocket
        async for message in ws:
            print(f"Message received: {message}")
            await onReceiveCallback(ws, message)
    except websockets.ConnectionClosedOK:
        print("Connection closed normally.")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed with an error: Code={e.code}, Reason={e.reason}")
    except Exception as e:
        print(f"Unexpected error in websocket_listener: {e}")

async def websocket_send(ws, message):
    result = False
    try:
        await ws.send(message)
        result = True
        print(f"Message sent successfully: {message}")
    except websockets.ConnectionClosed as e:
        print(f"WebSocket connection closed: Code={e.code}, Reason={e.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return result
