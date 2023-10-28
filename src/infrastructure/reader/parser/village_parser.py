import re
from typing import Callable
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, NavigableString, Tag

from src.domain.shared.village import Village, VillageBans
from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition
from src.exceptions.exceptions import IllegalArgumentsException
from src.utc_date import UtcDate


class VillageParser:
    def parse(self, content: bytes) -> Village:
        soup = BeautifulSoup(
            content,
            'html.parser',
            from_encoding='utf-8',
            exclude_encodings=[],
        )
        # もし、original が想定 encoding と異なる場合(今回は utf-8) に、
        # exclude_encodings に以下を設定することで解決できるケースがある。
        # ※ 指定しなければ response ヘッダの encoding が利用され、うまくパースできないことがあり、
        #    その解決策としてこのような方法をとっている。
        # print(soup.original_encoding)
        #
        # そのまま html 出力したい場合は以下で可能
        # print(str(soup))
        d1_element = self._find_or_throw(lambda: soup.find("div", class_="d1"))
        d11_element = self._find_or_throw(lambda: d1_element.find("div", class_="d11"))
        d11_element_text = d11_element.get_text(strip=True)

        return Village(
            self._to_village_number(d11_element_text),
            self._to_end_date(soup),
            self._to_name(d11_element_text),
            10,
            VillageCast.A,
            [VillageBans(VillagePosition.APOSTATE, "cc")],
        )

    def _to_village_number(self, d11_element_text: str) -> int:
        village_number = re.findall(r"No\.(\d+)「", d11_element_text)
        if not village_number[0]:
            raise IllegalArgumentsException()

        return int(village_number[0])

    def _to_end_date(self, soup: Tag) -> UtcDate:
        d12150_elements = soup.find_all("div", class_="d12150")
        if len(d12150_elements) < 1:
            raise IllegalArgumentsException()

        element: Tag = d12150_elements[1]
        try:
            return UtcDate.from_timezone_string(
                element.contents[0].get_text(),
                "%Y/%m/%d %H:%M:%S",
                ZoneInfo("Asia/Tokyo"),
            )
        except Exception as ex:
            raise IllegalArgumentsException("invalid html") from ex

    def _to_name(self, d11_element_text: str) -> str:
        name = re.findall(r"No\.\d+「(.+)」", d11_element_text)
        if not name[0]:
            raise IllegalArgumentsException()

        return name[0]

    def _find_or_throw(self, find: Callable) -> Tag:
        result = find()

        if not result or isinstance(result, NavigableString):
            raise IllegalArgumentsException()

        return result
