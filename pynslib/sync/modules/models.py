# This file is part of pynslib. pynslib is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version. pynslib is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. You should have received a copy of the GNU General Public License along
# with pynslib. If not, see <https://www.gnu.org/licenses/>.

from pynslib.sync.api import SyncAPI, NSAuth
from dataclasses import dataclass
from typing import Optional, Literal, List

cat_ids: dict = {
    "factbook": 1,
    "bulletin": 3,
    "account": 5,
    "meta": 8
}

subcat_ids: dict = {
    "overview": 100,
    "history": 101,
    "geography": 102,
    "factbook_culture": 103,
    "politics": 104,
    "legislation": 105,
    "religion": 106,
    "factbook_military": 107,
    "economy": 108,
    "international": 109,
    "trivia": 110,
    "miscellaneous": 111,
    "policy": 305,
    "news": 315,
    "opinion": 325,
    "campaign": 385,
    "account_military": 505,
    "trade": 515,
    "sport": 525,
    "drama": 535,
    "diplomacy": 545,
    "science": 555,
    "account_culture": 565,
    "other": 595,
    "gameplay": 835,
    "reference": 845,
}


@dataclass
class Dispatch:
    id: Optional[int]
    title: Optional[str]
    mode: Literal["add", "edit", "remove"]
    category: Optional[Literal["Factbook", "Bulletin", "Account", "Meta"]]
    subcategory: Optional[Literal[
        "Overview",
        "History",
        "Geography",
        "Factbook_Culture",
        "Politics",
        "Legislation",
        "Religion",
        "Factbook_Military",
        "Economy",
        "International",
        "Trivia",
        "Miscellaneous",
        "Policy",
        "News",
        "Opinion",
        "Campaign",
        "Account_Military",
        "Trade",
        "Sport",
        "Drama",
        "Diplomacy",
        "Science",
        "Account_Culture",
        "Other",
        "Gameplay",
        "Reference",
    ]]
    text: Optional[str]


class NationAPI:
    """
    The NationAPI object allows for private command manipulation of a nation
    through the NationStates API. You can create multiple instances of this
    object to manipulate multiple nations from the same program, and the library
    will maintain state appropriately for you.
    """
    __slots__ = (
        "api",
        "auth",
    )
    def __init__(self, api: SyncAPI, auth: NSAuth):
        self.api = api
        self.auth = auth

    def switch_context(self, *args, **kwargs):
        """
        Switches the context of the API to the nation represented by this object.
        This enables the use of private commands, such as dispatch, without
        destroying state you may be relying on elsewhere in your program.
        By default, this method is called automatically when you use a private
        command, but you can call it manually if you need to.

        :param args:
        :param kwargs:
        :return:
        """

        if self.api.auth:
            old_auth = self.api.auth
            self.api.auth = self.auth
            result = self.api.make(*args, **kwargs)
            self.api.auth = old_auth
            return result
        else:
            self.api.auth = self.auth
            return self.api.make(*args, **kwargs)


    def dispatch(self, dispatch: Dispatch):
        """
        Accepts a Dispatch object and dispatches it to the nation represented by
        this object. The Dispatch object can be created manually, or you can use
        the DispatchBuilder class to create one for you.

        :param dispatch:
        :return:
        """

        if dispatch.mode == "add":
            pass
        elif dispatch.mode == "edit":
            pass
        elif dispatch.mode == "remove":
            pass
