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
    from websocket_device_interface.desktop_specific.interface_handler import handler as wsInterfaceHandler



# Start the WebSocket server
async def main():
    await wsInterfaceHandler(80)
    pass


# Run the asyncio event loop and start the server
if __name__ == "__main__":
    asyncio.run(main())

