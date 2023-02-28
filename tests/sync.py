# This file is part of pynslib. pynslib is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version. pynslib is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. You should have received a copy of the GNU General Public License along
# with pynslib. If not, see <https://www.gnu.org/licenses/>.

import unittest
import pprint
import json
from pynslib.sync import SyncAPI, NSAuth


class CurrencyCase(unittest.TestCase):
    my_api = SyncAPI(useragent="NSLib Unit Tests // Dev: nation=united_calanworie")
    val = my_api.make({"nation": "astrellin", "q": "currency"})
    print(val)
    assert val["CURRENCY"] == "Ishar"


class DispatchCase(unittest.TestCase):
    my_api = SyncAPI(useragent="NSLib Unit Tests // Dev: nation=united_calanworie")
    val = my_api.make({"nation": "astrellin", "q": "dispatchlist"})
    with open("dispatchlist.json", "w") as w:
        json.dump(val, w)


class RatelimitTestCase(unittest.TestCase):
    """
    The ratelimit for the NS API is 50 requests in 30 seconds.
    To check that we do not receive a 429, we are going to make
    51 requests, and expect an error of type TooManyRequests.
    """

    my_api = SyncAPI(useragent="NSLib Unit Tests // Dev: nation=united_calanworie")
    for _ in range(51):
        my_api.mock()
        print(my_api.ratelimit_remaining)


if __name__ == "__main__":
    RatelimitTestCase()
