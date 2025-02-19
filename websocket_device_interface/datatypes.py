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

class WsRequest:
    def __init__(self, rawRequest):
        decoded = json.loads(rawRequest)
        self.uuid = decoded["UUID"]
        self.request = decoded["REQUEST"]
        
        self.fulfilled = False  # Indicates if the request is fulfilled
        self.response = None  # Holds the response data
        self.rawResponse = None
        self.executing = False
        self.toSend = False
        self.isSuccess = None

    def set_response(self, response, isSuccess):
        self.isSuccess = isSuccess
        outcome = "SUCCESS" if isSuccess else "ERROR"
        self.response = response
        self.rawResponse = json.dumps({"UUID": self.uuid, "RESPONSE": response, "OUTCOME": outcome})
        self.fulfilled = True
        self.toSend = True

    def is_fulfilled(self):
        return self.fulfilled

    def __repr__(self):
        return "WsRequest(uuid={}, request='{}', fulfilled={}, response='{}')".format(
            self.uuid, self.request, self.fulfilled, self.response
        )

class WsRequestList:
    def __init__(self, max_requests=10):
        self.requests = []  # List to hold all WsRequests
        self.max_requests = max_requests

    def add_request(self, request):
        """
        Adds a new WsRequest to the list if the UUID is not already present
        and the limit is not exceeded. If the limit is reached, removes the oldest
        fulfilled request; if all requests are unfulfilled, removes the oldest request.
        Returns True if the request is added successfully, False if the UUID already exists.
        """
        # Check if request with the same UUID already exists
        if self.get_request_by_uuid(request.uuid) is not None:
            existing_request = self.get_request_by_uuid(request.uuid)
            if existing_request.executing:
                print("still executing")
            else:
                existing_request.toSend = True
            print("Duplicate request")
            return False  # UUID already in pending requests, do not add

        if len(self.requests) >= self.max_requests:
            # Find the oldest fulfilled request, if any
            oldest_fulfilled = None
            for req in self.requests:
                if req.is_fulfilled():
                    oldest_fulfilled = req
                    break
            
            if oldest_fulfilled:
                self.requests.remove(oldest_fulfilled)
            else:
                # If all are unfulfilled, remove the oldest request
                self.requests.pop(0)

        self.requests.append(request)
        return True

    def get_request_by_uuid(self, request_uuid):
        """Finds and returns a request by UUID, or None if not found."""
        for req in self.requests:
            if req.uuid == request_uuid:
                return req
        return None

    def mark_request_fulfilled(self, request_uuid):
        """Marks a request as fulfilled by UUID. Returns True if successful."""
        request = self.get_request_by_uuid(request_uuid)
        if request:
            request.set_response("Fulfilled", True)
            return True
        return False

    def get_fulfilled_requests(self):
        """Returns a list of all fulfilled requests."""
        return [req for req in self.requests if req.is_fulfilled()]

    def get_unfulfilled_requests(self):
        """Returns a list of all unfulfilled requests."""
        return [req for req in self.requests if not req.is_fulfilled()]

    def remove_request(self, request_uuid):
        """Removes a request by UUID. Returns True if successful."""
        request = self.get_request_by_uuid(request_uuid)
        if request:
            self.requests.remove(request)
            return True
        return False

    def __repr__(self):
        return "WsRequestList({}/{} requests)".format(len(self.requests), self.max_requests)


