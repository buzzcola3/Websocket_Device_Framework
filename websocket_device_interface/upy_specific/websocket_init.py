import asyncio
from microdot import Microdot # type: ignore
from microdot.websocket import with_websocket

from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequestList
from Websocket_Device_Framework.websocket_device_interface.request_transceiver import handle_receive
from Websocket_Device_Framework.websocket_device_interface.upy_specific.interface_handler import websocket_receive, websocket_send



async def handler():
    free_port = 80
    print("handler")
    
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
