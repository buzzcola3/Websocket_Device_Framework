import asyncio
from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequest, WsRequestList
from Websocket_Device_Framework.websocket_device_interface.request_executor import handle_execute

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

async def handle_receive(ws, message):
    print("handleRX")
    ws_request = WsRequest(message)
    ws_request_list.add_request(ws_request)
    print("starting execute task")
    asyncio.create_task(execute_and_send(ws))


async def handle_send(ws):
    for request in ws_request_list.requests:
        if request.toSend:
            request.toSend = False
            await websocket_send(ws, request.rawResponse)

        

async def execute_and_send(ws):
    await handle_execute(ws, ws_request_list)
    await handle_send(ws)