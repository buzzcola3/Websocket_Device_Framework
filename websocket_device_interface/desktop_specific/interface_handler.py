# Main WebSocket handler that manages both sending and receiving
import asyncio
import websockets

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequestList
from Websocket_Device_Framework.websocket_device_interface.desktop_specific.request_transceiver import handle_send, handle_receive
from Websocket_Device_Framework.websocket_device_interface.request_executor import handle_execute


wsRequestList = WsRequestList(max_requests = 64)

async def wsHandler(ws):
        

        try:
            await asyncio.gather(
                handle_receive(ws, wsRequestList),
                handle_send(ws, wsRequestList),
                handle_execute(wsRequestList)
            )  # Run both sending and receiving concurrently
        except websockets.ConnectionClosedOK:
            print("Connection closed normally")
        except websockets.ConnectionClosedError:
            print("Connection closed with an error")
        except Exception as e:
            print(f"Error in handler: {e}")

async def handler(port):
    async with websockets.serve(wsHandler, "localhost", port):
        print(f"Server started on localhost:{port}")
        await asyncio.Future()  # Run indefinitely
