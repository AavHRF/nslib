# This file is part of nslib. nslib is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version. nslib is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. You should have received a copy of the GNU General Public License along
# with nslib. If not, see <https://www.gnu.org/licenses/>.

import requests
import time
from typing import Optional, List
from requests.auth import AuthBase
from .modules import Parser

PRIVATE_SHARDS: List[str] = [
    "dossier",
    "issues",
    "issuesummary",
    "nextissue",
    "nextissuetime",
    "notices",
    "packs",
    "ping",
    "rdossier",
    "unread",
]

PRIVATE_COMMANDS: List[str] = [
    "issue",
    "giftcard",
    "dispatch",
    "rmbpost",
]


class RateLimitExceeded(Exception):
    pass


class NoAuthSet(Exception):
    pass


class NSAuth(AuthBase):
    def __init__(self, nation: str, password: str):
        self.nation = nation
        self.password = password
        self._pin = None

    def __call__(self, request: requests.PreparedRequest):
        request.headers["X-Password"] = self.password
        if self._pin:
            request.headers["X-Pin"] = self._pin
        return request

    @property
    def pin(self) -> Optional[str]:
        return self._pin

    @pin.setter
    def pin(self, xpin: str):
        self._pin = xpin


class SyncAPI:
    def __init__(self, useragent: str, auth: Optional = None):
        self.useragent = useragent
        self.auth = auth
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.useragent})
        self.api_url = "https://www.nationstates.net/cgi-bin/api.cgi"

        # Ratelimit variables
        self.ratelimit_remaining = 0
        self.ratelimit_reset = 0
        self.last_request_time = 0
        self.maximum_requests = 45  # Undershoot the API limit by 5 requests to be safe.

    def _limit(self) -> bool:
        """
        Limits the requests to the API to no more than 50 every 30 seconds.
        The usage of these 50 requests in any 30-second period is irrelevant.
        You can burst up to the maximum requests allowed as long as 50/30 is not
        exceeded.

        :return: A boolean value of if the request can proceed.
        """
        now = time.time()
        if now - self.last_request_time <= 30:
            if self.ratelimit_remaining > 0:
                self.ratelimit_remaining -= 1
                self.last_request_time = now
                return True
            else:
                return False
        else:
            if self.ratelimit_remaining > 0:
                self.ratelimit_remaining = self.maximum_requests
                self.ratelimit_remaining -= 1
                self.last_request_time = now
                return True
            else:
                return False

    def _request(
        self, params: dict, method: str = "GET", isprivate: bool = False
    ) -> requests.Response:
        """
        Makes a request to the API.

        :param params: The parameters to send to the API.
        :param method: The HTTP method to use.
        :param isprivate: If the request is private.
        :return: The response from the API.
        """
        if not self._limit():
            raise RateLimitExceeded
        if isprivate:
            return self.session.request(
                method, self.api_url, params=params, auth=self.auth
            )
        else:
            return self.session.request(method, self.api_url, params=params)

    def make(self, params: dict) -> dict:
        """
        Makes a request to the API and parses the response.

        :param params: The parameters to send to the API.
        :return: The parsed response from the API.
        """
        isprivate = False
        if "q" in params:
            if params["q"] in PRIVATE_COMMANDS:
                isprivate = True
            else:
                isprivate = False
        if "c" in params:
            isprivate = True
        else:
            isprivate = False

        # Guard against no auth being set
        if isprivate:
            if not self.auth:
                raise NoAuthSet

        response = self._request(params, isprivate=isprivate)
        if isprivate:
            if self.auth.pin is None:
                # If the PIN is not set, set it.
                self.auth.pin = response.headers["X-Pin"]
            else:
                if response.headers["X-Pin"] != self.auth.pin:
                    # Update our pin if the session has changed.
                    self.auth.pin = response.headers["X-Pin"]
        return Parser(response.text)()

    def nation(self, nation: str) -> dict:
        """
        Gets the nation data for a nation.

        :param nation: The nation to get the data for.
        :return: The parsed response from the API.
        """
        params = {
            "nation": nation,
        }
        return self.make(params)

    def region(self, region: str) -> dict:
        """
        Gets the region data for a region.

        :param region: The region to get the data for.
        :return: The parsed response from the API.
        """
        params = {
            "region": region,
        }
        return self.make(params)

    @staticmethod
    def _create_auth(nation: str, password: str) -> NSAuth:
        """
        Creates an authentication object for the API.

        :param nation: The nation to authenticate as.
        :param password: The password to use.
        :return: The authentication object.
        """
        auth = NSAuth(nation, password)
        return auth

    def mock(self) -> int:
        """
        Mock function to test the ratelimit.
        :return:
        """
        if not self._limit():
            raise RateLimitExceeded
        return 1
