# This file is part of nslib. nslib is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version. nslib is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. You should have received a copy of the GNU General Public License along
# with nslib. If not, see <https://www.gnu.org/licenses/>.

from .api import SyncAPI
from dataclasses import dataclass
from typing import Optional, Literal

cat_ids: dict = {
    "factbook": 1,
    "bulletin": 3,
    "account": 5,
    "meta": 8
}

subcat_ids: dict = {
    "Overview": 100,
    "History": 101,
    "Geography": 102,
    "Factbook_Culture": 103,
    "Politics": 104,
    "Legislation": 105,
    "Religion": 106,
    "Factbook_Military": 107,
    "Economy": 108,
    "International": 109,
    "Trivia": 110,
    "Miscellaneous": 111,
    "Policy": 305,
    "News": 315,
    "Opinion": 325,
    "Campaign": 385,
    "Account_Military": 505,
    "Trade": 515,
    "Sport": 525,
    "Drama": 535,
    "Diplomacy": 545,
    "Science": 555,
    "Account_Culture": 565,
    "Other": 595,
    "Gameplay": 835,
    "Reference": 845,
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


class Nation:
    def __init__(self, api: SyncAPI, nation: str):
        self.api = api
        self.nation = nation

    def dispatch(self, dispatch: Dispatch):
        if dispatch.mode == "add":
            pass
        elif dispatch.mode == "edit":
            pass
        elif dispatch.mode == "remove":
            pass
