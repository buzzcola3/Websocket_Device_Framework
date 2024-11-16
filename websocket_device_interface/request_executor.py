import asyncio
import json

from Websocket_Device_Framework.commands import command_devinfo, command_ping
from device_specific.device import runDeviceCommand

async def handle_execute(wsRequestList):
    """Continuously processes each request in the WsRequestList by executing its command."""
    print("Starting handle_execute task...")

    while True:  # Infinite loop to keep retrying if there's an error
        try:
            # Loop through each request in the list
            for request in wsRequestList.requests:
                if not request.fulfilled:
                    if not request.executing:
                        request.executing = True

                        try:
                            request.request = json.loads(request.request)

                            if request.request["COMMAND"] == "GET_STATUS":
                                uuid = request.request["PARAMETERS"][0]
                                relevantRequest = wsRequestList.get_request_by_uuid(uuid)

                                if relevantRequest is None:
                                    request.set_response("UNEXISTENT", True)
                                elif not relevantRequest.fulfilled:
                                    request.set_response("PENDING", True)
                                elif relevantRequest.fulfilled:
                                    request.set_response("FULFILLED", True)
                                else:
                                    request.set_response("ERROR", False)

                                request.executing = False
                                continue

                            elif request.request["COMMAND"] == "GET_RESULT":
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

                            elif request.request["COMMAND"] == "PING":
                                response = command_ping()
                                request.set_response(response, True)

                                request.executing = False
                                continue

                            elif request.request["COMMAND"] == "DEVINFO":
                                response = command_devinfo()
                                request.set_response(response, True)

                                request.executing = False
                                continue

                            elif not request.fulfilled:
                                response, isSuccess = await runDeviceCommand(request.request["COMMAND"], request.request["PARAMETERS"])
                                request.set_response(response, isSuccess)

                                request.executing = False
                                continue
                        except Exception as e:
                            print(f"Error processing request {request.request}: {e}")
                            request.executing = False
                            continue  # Continue with the next request in case of failure

            # Add a small delay to prevent the loop from running continuously without rest
            await asyncio.sleep(0.1)

        except Exception as e:
            # If any error occurs during the execution loop, restart the entire function
            print(f"Error in handle_execute: {e}. Restarting execution loop...")
            await asyncio.sleep(2)  # Optional: Add a small delay before retrying to avoid rapid retries

