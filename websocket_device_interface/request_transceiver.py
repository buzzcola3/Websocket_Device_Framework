import asyncio
from Websocket_Device_Framework.websocket_device_interface.datatypes import WsRequest
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
    



async def handle_receive(ws, ws_request_list):
    received_data = await websocket_receive(ws)
    for message in received_data:
        ws_request = WsRequest(message)
        ws_request_list.add_request(ws_request)
    asyncio.create_task(execute_and_send(ws, ws_request_list))


async def handle_send(ws, ws_request_list):
    for request in ws_request_list.requests:
        if request.toSend:
            request.toSend = False
            await websocket_send(ws, request.rawResponse)

        

async def execute_and_send(ws, ws_request_list):
    success = await handle_execute(ws_request_list)
    await handle_send(ws, ws_request_list)