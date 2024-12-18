import asyncio
from microdot import Microdot # type: ignore

async def websocket_receive(ws, onReceiveCallback):
    """
    Listens to the WebSocket and calls callback funcion on every new message
    """
    try:
        # Continuously listen for messages from the WebSocket
        async for message in ws:
            print(f"Message received: {message}")
            await onReceiveCallback(ws, message)
    except websockets.ConnectionClosedOK:
        print("Connection closed normally.")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed with an error: Code={e.code}, Reason={e.reason}")
    except Exception as e:
        print(f"Unexpected error in websocket_listener: {e}")

async def websocket_send(ws, message):
    result = False
    try:
        await ws.send(message)
        result = True
        print(f"Message sent successfully: {message}")
    except websockets.ConnectionClosed as e:
        print(f"WebSocket connection closed: Code={e.code}, Reason={e.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return result

