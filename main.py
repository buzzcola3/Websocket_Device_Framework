import asyncio

try:
    import machine # type: ignore
    IS_MICROPYTHON = True
except:
    IS_MICROPYTHON = False

if IS_MICROPYTHON:
    from Websocket_Device_Framework.websocket_device_interface.upy_specific.websocket_init import handler
    
    from device_specific.setup_wifi import connect_wifi # type: ignore
    connect_wifi()
else:
    from Websocket_Device_Framework.websocket_device_interface.desktop_specific.websocket_init import handler



# Start the WebSocket server
async def main():
    await handler()


asyncio.run(main())