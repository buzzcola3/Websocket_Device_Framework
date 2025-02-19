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

from Websocket_Device_Framework.commands import command_devinfo, command_ping
from device_specific.device import runDeviceCommand

async def handle_execute(ws, wsRequestList):
    """Continuously processes each request in the WsRequestList by executing its command."""
    print("Starting handle_execute...")

    result = None

    try:
        # Loop through each request in the list
        for request in wsRequestList.requests:
            if not request.fulfilled and not request.executing:
                request.executing = True
                try:
                    if result == None:
                        result = True

                    request.request = json.loads(request.request) if isinstance(request.request, str) else request.request
                    if request.request["COMMAND"] == "GET_RESULT":
                        uuid = request.request["PARAMETERS"][0]
                        relevantRequest = wsRequestList.get_request_by_uuid(uuid)
                        if relevantRequest is None:
                            request.set_response("UNEXISTENT", False)
                        elif relevantRequest.fulfilled:
                            request.set_response(relevantRequest.response, relevantRequest.isSuccess)
                        else:
                            request.set_response("ERROR", False)
                        request.executing = False
                        continue
                    if request.request["COMMAND"] == "PING":
                        response = command_ping()
                        request.set_response(response, True)
                        request.executing = False
                        continue
                    if request.request["COMMAND"] == "DEVINFO":
                        response = command_devinfo()
                        request.set_response(response, True)
                        request.executing = False
                        continue
                    if not request.fulfilled:
                        response, isSuccess = await runDeviceCommand(request.request["COMMAND"], request.request["PARAMETERS"])
                        print(response)
                        request.set_response(response, isSuccess)
                        request.executing = False
                        continue
                except Exception as e:
                    result = False
                    print(f"Error processing request {request.request}: {e}")
                    request.executing = False
                    continue  # Continue with the next request in case of failure

    except Exception as e:
        result = False
        # If any error occurs during the execution
        print(f"Error in handle_execute: {e}.")
    return result

