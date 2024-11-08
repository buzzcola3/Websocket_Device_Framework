# Main WebSocket handler that manages both sending and receiving
import asyncio
from microdot import Microdot # type: ignore
from microdot.websocket import with_websocket

from websocket_device_interface.datatypes import WsRequestList
from websocket_device_interface.upy_specific.request_transceiver import handle_send, handle_receive
from websocket_device_interface.request_executor import handle_execute


wsRequestList = WsRequestList(max_requests = 64)

async def wsHandler():
    while True:
        if externalWs is not None:
            #print("hum")
            pass
        await asyncio.sleep(0.1)

externalWs = None
asyncio.create_task(wsHandler())
asyncio.create_task(handle_execute(wsRequestList))
asyncio.create_task(handle_send(wsRequestList))




async def handler(port):
    global externalWs  # Declare externalWs as global within the function to assign it

    print(port)
    # Start the WebSocket server on localhost
    app = Microdot()
    
    @app.route('/')
    @with_websocket  # type: ignore
    async def echo(request, ws):
        while True:
            global externalWs  # Use the global variable here
            if externalWs is None:
                externalWs = ws  # Assign ws to externalWs
            await handle_receive(ws, wsRequestList)
            #await handle_send(wsRequestList)
            
            # Create a task to run wsHandler with ws
            
        
    # Start the server (assuming the app has a start method; adjust as necessary)
    app.run(port=port)
