# This file is part of pynslib. pynslib is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version. pynslib is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. You should have received a copy of the GNU General Public License along
# with pynslib. If not, see <https://www.gnu.org/licenses/>.

import asyncio
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError
from typing import List, Dict, Any, Union


class AsyncParser:
    """
    Parses XML from the NS API and returns it as a JSON object.
    """

    def __init__(self, xml: str):
        """
        Parser constructor
        :param xml: The XML to parse.
        """
        self.xml = xml

    async def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        return await self.parse()

    async def parse(self) -> Dict[str, Any]:
        """
        Parses the XML and returns it as a JSON object.
        :return: The JSON object.
        """
        try:
            root = ET.fromstring(self.xml)
        except ParseError:
            return {}
        return await asyncio.to_thread(self._parse_element, root)

    def _parse_element(
        self, element: ET.Element
    ) -> Union[Dict[str, Any], List[Union[str, Dict[str, Any]]]]:
        """
        Parses a single XML element and returns it as a JSON object.
        :param element: The element to parse.
        :return: The JSON object.
        """
        # If the element has no children, return it flat
        if len(element) == 0:
            return {element.tag: element.text}

        # If the element has children, return a dictionary.
        result = {}
        for child in element:
            # If the child is a list, add it to the list.
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(self._parse_element(child))
                else:
                    result[child.tag] = [result[child.tag], self._parse_element(child)]
            # If the child is not a list, add it to the dictionary.
            else:
                if len(child) == 0:
                    result[child.tag] = child.text
                else:
                    result[child.tag] = self._parse_element(child)
        return result
