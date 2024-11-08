import asyncio

from websocket_device_interface.datatypes import WsRequest, WsRequestList


externalWs = None
# WebSocket handler for receiving messages
async def handle_receive(ws, wsRequestList):
    global externalWs
    externalWs = ws
    
    message = await ws.receive()
    print("Received:", message)
            # Add parsed command to the command buffer
    wsRequest = WsRequest(message)
    wsRequestList.add_request(wsRequest)



async def handle_send(wsRequestList):
    while(1):
        for request in wsRequestList.requests:
            if request.toSend:
                request.toSend = False
                print(request.rawResponse)
                await externalWs.send(request.rawResponse)
        await asyncio.sleep(0.01)
    


