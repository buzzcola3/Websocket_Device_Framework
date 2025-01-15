import asyncio
from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequest, WsRequestList
from Websocket_Device_Framework.websocket_device_interface.request_executor import handle_execute
from Websocket_Device_Framework.commands import command_devinfo, command_ping
from jsonrpc import JSONRPCResponseManager, dispatcher

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

@dispatcher.add_method
def DEVINFO(**kwargs):
    return command_devinfo()


async def handle_receive(ws, message):
    print("handleRX")
    if(message == "ping"):
        await handle_send(ws, "pong")
        return

    response = JSONRPCResponseManager.handle(message, dispatcher)
    asyncio.create_task(handle_send(ws, response.json))


async def handle_send(ws, message):
    await websocket_send(ws, message)

        

async def execute_and_send(ws):
    await handle_execute(ws, ws_request_list)
    await handle_send(ws)