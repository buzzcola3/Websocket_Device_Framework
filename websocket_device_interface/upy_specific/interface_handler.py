# Main WebSocket handler that manages both sending and receiving
import asyncio
from microdot import Microdot # type: ignore
from microdot.websocket import with_websocket

from websocket_device_interface.datatypes import WsRequestList
from websocket_device_interface.upy_specific.request_transceiver import handle_send, handle_receive
from websocket_device_interface.request_executor import handle_execute


wsRequestList = WsRequestList(max_requests = 64)


externalWs = None



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

            success = handle_receive(ws, wsRequestList)
            #TODO INSTANT ECHO
            if success:
                # Create a task to run handle_execute
                asyncio.run(handle_execute(WsRequestList))
            
            # Create a task to run wsHandler with ws
        
    # Start the server (assuming the app has a start method; adjust as necessary)
    app.run(port=port)

async def execute_and_send(wsRequestList):
    success = await handle_execute(wsRequestList)
    if success:
        await handle_send(wsRequestList)
