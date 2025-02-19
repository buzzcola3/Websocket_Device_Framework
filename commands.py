# Copyright 2025 Samuel Betak
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

try:
    import machine  # type: ignore
    IS_MICROPYTHON = True
except ImportError:
    import uuid  # Standard Python module
    IS_MICROPYTHON = False

# Device-specific imports
from device_specific.device import getDeviceName, getDeviceDescription, getDeviceAvailableCommands, getDeviceAvailableNodes
from Websocket_Device_Framework.small_tools import get_file_as_string

def generate_uuid():
    if IS_MICROPYTHON:
        # Generate a unique ID on MicroPython (e.g., ESP32)
        unique_id = machine.unique_id()  # Returns bytes specific to the device
        return ''.join('{:02x}'.format(byte) for byte in unique_id)
    else:
        # Generate a UUIDv1 on desktop Python
        return str(uuid.uuid1())

def get_unique_id():
    file_path = "./device_specific/device_info.json"
    
    # Try to open the file to check if it exists
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data["UNIQUE_ID"]
    except OSError:
        # If the file doesn't exist, OSError will be raised
        unique_id = generate_uuid()
        data = {"UNIQUE_ID": unique_id}
        with open(file_path, 'w') as f:
            json.dump(data, f)
        return unique_id

# The command_devinfo function, now using get_unique_id for UNIQUE_ID
def command_devinfo():    
    return json.dumps({
        "UNIQUE_ID": get_unique_id(),
        "DEVICE_NAME": getDeviceName(),
        "DEVICE_DESCRIPTION": getDeviceDescription(),
        "DEVICE_AVAILABLE_COMMANDS": getDeviceAvailableCommands(),
        "DEVICE_AVAILABLE_NODES": getDeviceAvailableNodes(),
        "DEVICE_ICON_SVG": get_file_as_string("./device_specific/device_icon.svg"),
    })

def command_ping():
    print("PINGED")
    return "OK"

