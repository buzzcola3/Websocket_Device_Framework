# WebSocket Device Framework

The WebSocket Device Framework is a versatile, cross-platform framework designed to enable request-based WebSocket communication with devices. It can be run on both **CPython** and **MicroPython**, providing a flexible solution for connecting and controlling devices via WebSockets.

The goal is to quickly adapt any device or tool, regardless of its underlying protocol, to work seamlessly as a WebSocket-enabled device. Ideally, this integration can be achieved in a matter of minutes.

---

## Features

- **Real-time request-based control**: Send commands and receive responses instantly via WebSocket.
- **Unique device IDs**: Each device is assigned a unique identifier on its first run.
- **Duplicate message detection**: Prevents the processing of duplicate WebSocket messages.
- **Easy setup**: Simply add your `device_specific` folder (see [example](#)), run `main.py`, and you're ready to go.

---

## Setup

### 1. Add your `device_specific` folder

Create a `device_specific` folder with your device's specific logic. You can find an [example folder here](#). This folder will contain all the necessary code to interface with your particular device.

### 2. Run `main.py`

Once the `device_specific` folder is in place, simply run the `main.py` script to start the WebSocket server.

```bash
python main.py
```

### 3. Connect via WebSocket

Connect to your device using a compatible WebSocket client. The WebSocket server will be running on the device's IP address, allowing you to send commands and interact with your device.

## Usage

Connect to the IP address of the device using a WebSocket client and send your commands