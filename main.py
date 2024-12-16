import asyncio

try:
    import machine # type: ignore
    IS_MICROPYTHON = True
except:
    IS_MICROPYTHON = False

if IS_MICROPYTHON:
    from websocket_device_interface.upy_specific.interface_handler import handler as wsInterfaceHandler
    
    from device_specific.setup_wifi import connect_wifi # type: ignore
    connect_wifi()
else:
    from Websocket_Device_Framework.websocket_device_interface.desktop_specific.interface_handler import handler as wsInterfaceHandler



# Start the WebSocket server
async def main():
    await wsInterfaceHandler()


# Run the asyncio event loop and start the server

asyncio.run(main())