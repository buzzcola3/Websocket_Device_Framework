import asyncio
import websockets

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequest, WsRequestList


async def handle_receive(ws, wsRequestList):
    while True:  # Infinite loop to keep retrying if there's an error or connection issue
        try:
            async for message in ws:  # This automatically handles connection closure
                print("Received:", message)
                # Add parsed command to the command buffer
                await asyncio.sleep(0.01)
                wsRequest = WsRequest(message)
                wsRequestList.add_request(wsRequest)
                
        except websockets.ConnectionClosedOK:
            print("Connection closed normally for receiving.")
            break  # Stop retrying if the connection is closed normally.
            
        except websockets.ConnectionClosedError:
            print("Connection closed with an error during receiving. Retrying...")
        
        except Exception as e:
            await asyncio.sleep(2)
            print(f"Error in receiving: {e}. Retrying...")
            


async def handle_send(ws, wsRequestList):
    while True:  # Infinite loop to keep retrying if there's an error or connection issue
        try:
            while True:  # Inner loop to process requests continuously
                for request in wsRequestList.requests:
                    if request.toSend:
                        request.toSend = False
                        await ws.send(request.rawResponse)
                        await asyncio.sleep(0.01)
                await asyncio.sleep(0.01)  # Prevent 100% CPU usage in idle time
        except websockets.ConnectionClosedOK:
            print("Connection closed normally for sending.")
            break  # Stop retrying if the connection is closed normally.
        except websockets.ConnectionClosedError:
            print("Connection closed with an error during sending. Retrying...")
        except Exception as e:
            await asyncio.sleep(2)
            print(f"Error in sending: {e}. Retrying...")
        
