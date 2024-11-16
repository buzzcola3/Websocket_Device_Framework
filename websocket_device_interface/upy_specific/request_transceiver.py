import asyncio

from websocket_device_interface.datatypes import WsRequest, WsRequestList


externalWs = None
# WebSocket handler for receiving messages
async def handle_receive(ws, wsRequestList):
    global externalWs
    externalWs = ws  # Store the WebSocket instance
    
    while True:  # Outer loop to continuously receive messages
        try:
            # Attempt to receive a message
            message = await ws.receive()
            print("Received:", message)
            
            # Parse the message and add it to the request list
            wsRequest = WsRequest(message)
            wsRequestList.add_request(wsRequest)
        
        except Exception as e:
            err = True
            # Log any other unexpected exceptions
            print(f"Error receiving message: {e}. Retrying...")
            await asyncio.sleep(2)
        
            



async def handle_send(wsRequestList, externalWs):
    """Handles sending requests from wsRequestList to external WebSocket."""
    while True:  # Outer loop to keep retrying if there's an error
        try:
            for request in wsRequestList.requests:
                if request.toSend:
                    request.toSend = False
                    try:
                        print(request.rawResponse)
                        await externalWs.send(request.rawResponse)
                    except Exception as e:
                        # Catch any error that occurs when sending
                        print(f"Error sending request {request.rawResponse}: {e}")
                        continue  # Skip to next request in case of error
            # Add a small delay to prevent the loop from running continuously without rest
            await asyncio.sleep(0.01)
        
        except Exception as e:
            # If an error occurs in the outer loop, restart the sending process
            print(f"Error in handle_send: {e}. Restarting send handler...")
            await asyncio.sleep(2)
    


