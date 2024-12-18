import asyncio
import websockets
import socket


async def websocket_receive(ws):
    result = []
    try:
        print("here1")
        # Try to gather all messages that are currently available
        while True:
            try:
                # Receive a message from the websocket if it's available
                message = await asyncio.wait_for(ws.recv(), timeout=0.1)  # Adjust timeout as needed
                result.append(message)
                print("rx")
            except asyncio.TimeoutError:
                # No more messages in the buffer, exit the loop
                break
        
    except websockets.ConnectionClosedOK:
        print("Connection closed normally for receiving.")
        
    except websockets.ConnectionClosedError:
        print("Connection closed with an error during receiving. Retrying...")
    
    except Exception as e:
        print(f"Error in receiving: {e}. Retrying...")

    return result

async def websocket_send(ws, message):
    result = False
    try:
        print(f"sent: {message}")
        await ws.send(message)
        result = True
    except websockets.ConnectionClosedOK:
        print("Connection closed normally for sending.")
    except websockets.ConnectionClosedError:
        print("Connection closed with an error during sending. Retrying...")
    except Exception as e:
        print(f"Error in sending: {e}.")
    return result