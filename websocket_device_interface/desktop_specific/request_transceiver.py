import asyncio
import websockets

from websocket_device_interface.datatypes import WsRequest, WsRequestList


# WebSocket handler for receiving messages
async def handle_receive(ws, wsRequestList):
    try:
        async for message in ws:  # Automatically handles connection closure
            print("Received:", message)
            # Add parsed command to the command buffer
            await asyncio.sleep(0.01)
            wsRequest = WsRequest(message)
            wsRequestList.add_request(wsRequest)

    except websockets.ConnectionClosedOK:
        print("Connection closed normally for receiving")

    except websockets.ConnectionClosedError:
        print("Connection closed with an error during receiving")

    except Exception as e:
        print(f"Error in receiving: {e}")


async def handle_send(ws, wsRequestList):
    try:
        while True:
            for request in wsRequestList.requests:
                if request.toSend:
                    request.toSend = False
                    await ws.send(request.rawResponse)
                    await asyncio.sleep(0.01)
            await asyncio.sleep(0.01)
    except websockets.ConnectionClosedOK:
        print("Connection closed normally for sending")
    except websockets.ConnectionClosedError:
        print("Connection closed with an error during sending")
    except Exception as e:
        print(f"Error in sending: {e}")
