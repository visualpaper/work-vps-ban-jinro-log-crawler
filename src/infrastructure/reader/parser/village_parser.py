import re
from dataclasses import dataclass
from typing import Callable, List, Optional
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, NavigableString, Tag

from src.domain.shared.village import Village, VillageBans
from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition
from src.exceptions.exceptions import IllegalArgumentsException
from src.utc_date import UtcDate


@dataclass(frozen=True)
class VillagePlayer:
    name: str
    trip: str
    position: Optional[VillagePosition]

    def same_bame(self, name: str) -> bool:
        return self.name == name


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

        village_number: int = self._to_village_number(d11_element_text)
        players: List[VillagePlayer] = self._to_players(soup)
        bans_player_names: List[str] = []
        bans_player_names = self._to_bans_player_names_old(soup, village_number)

        return Village(
            village_number,
            self._to_end_date(soup, village_number),
            self._to_name(d11_element_text),
            len(players),
            self._to_cast(d11_element_text, village_number),
            self._to_village_bans(bans_player_names, players),
        )

    def _to_village_number(self, d11_element_text: str) -> int:
        village_number = re.findall(r"No\.(\d+)「", d11_element_text)
        if not village_number[0]:
            raise IllegalArgumentsException()

        return int(village_number[0])

    def _to_end_date(self, soup: Tag, village_number: int) -> UtcDate:
        d12150_elements = soup.find_all("div", class_="d12150")
        if len(d12150_elements) < 1:
            raise IllegalArgumentsException()

        # 223280 依然は d12150 の 1 番要素から、
        # 223280 以降は d12150 の 0 番要素から取れる。
        element: Tag = (
            d12150_elements[1] if village_number < 223280 else d12150_elements[0]
        )
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

    def _to_cast(self, d11_element_text: str, village_number: int) -> VillageCast:
        # 244434 以前は役職[*] から、
        # 244434 からは[配役*] から取れる。
        if village_number < 244434:
            cast = re.findall(r"役職\[([A-D]|Z)\]", d11_element_text)
            if not cast[0]:
                raise IllegalArgumentsException()

            return VillageCast.of(cast[0])

        cast = re.findall(r"\[配役([A-D]|Z)\]", d11_element_text)
        if not cast[0]:
            raise IllegalArgumentsException()

        return VillageCast.of(cast[0])

    def _is_player(self, name_element: Tag) -> bool:
        result = re.findall("【", name_element.get_text())

        return len(result) == 1

    def _to_player(self, name_element: Tag) -> tuple[str, str]:
        splited = name_element.get_text().split("【")
        if len(splited) != 2:
            raise IllegalArgumentsException()

        return splited[0], "【" + splited[1]

    def _to_position(self, value: str) -> Optional[VillagePosition]:
        if value == "決定前":
            return None

        try:
            return VillagePosition.of(value.replace("　", ""))
        except IllegalArgumentsException as ex:
            raise IllegalArgumentsException(value) from ex

    def _to_players(self, soup: Tag) -> List[VillagePlayer]:
        iconsmall_element = soup.find("table", class_="iconsmall")
        if not iconsmall_element or isinstance(iconsmall_element, NavigableString):
            raise IllegalArgumentsException()

        name_elements = iconsmall_element.find_all("td", class_="name")
        players: List[tuple[str, str]] = [
            self._to_player(name_element)
            for name_element in name_elements
            if self._is_player(name_element)
        ]

        regex = re.compile("^oc.+")
        val_elements = iconsmall_element.find_all("span", {"class": regex})
        if not val_elements or isinstance(val_elements, NavigableString):
            # 開始前の廃村時に一人もいないケースがあり得るため、そういった村は無視する。
            #            raise IllegalArgumentsException()
            return []

        positions = [
            self._to_position(val_element.get_text(strip=True))
            for val_element in val_elements
        ]
        # 【】が名前やトリップにある場合に問題になるため、そういったプレイヤーは無視する。
        #        if len(players) != len(positions):
        #            raise IllegalArgumentsException()

        result = []
        for i, player in enumerate(players):
            result.append(VillagePlayer(player[0], player[1], positions[i]))

        return result

    def _to_bans_player_names_old(self, soup: Tag, village_number: int) -> List[str]:
        d12151_elements = soup.find_all("div", class_="d12151")

        # 223280 依然は d12151 の 1 番要素から、
        # 223280 以降は d12151 の 0 番要素から取れる。
        elements = d12151_elements[1] if village_number < 223280 else d12151_elements[0]
        if not elements or isinstance(elements, NavigableString):
            raise IllegalArgumentsException()

        cvtd_element = elements.find("td", class_="cv")
        if not cvtd_element or isinstance(cvtd_element, NavigableString):
            # 村番号 255121 までは迷惑者通報以外にも通報結果が表示されている。
            # 村番号 255122 からは迷惑者のみが表示されるようになっている。
            if village_number < 255122:
                raise IllegalArgumentsException()

            return []

        # 村番号 255121 までは迷惑者通報以外にも通報結果が表示されている。
        # 通報がある場合は、IP が表示される仕組みとなっている。
        tr_elements = cvtd_element.select("table > tbody > tr")
        return [
            tr_element.contents[0].get_text()
            for tr_element in tr_elements
            if tr_element.contents[2].get_text(strip=True) != ""
        ]

    def _to_village_bans(
        self, bans_player_names: List[str], players: List[VillagePlayer]
    ) -> List[VillageBans]:
        result = []

        # 開始前の場合は、仮に通報対象者がいても何もしない。
        if any(player.position is None for player in players):
            return []

        for bans_player_name in bans_player_names:
            # 通報対象者かどうかの判断は Trip でなく player 名で実施しか判断できない。
            # そのため、もし、同名称のものがあると誤った結果となってしまう可能性があるため、
            # そのような場合は ban 者はいないと見做す。
            target = [
                player for player in players if player.same_bame(bans_player_name)
            ]
            if len(target) == 1:
                if target[0].position is None:
                    raise IllegalArgumentsException()

                result.append(VillageBans(target[0].position, target[0].trip))

        return result

    def _find_or_throw(self, find: Callable) -> Tag:
        result = find()

        if not result or isinstance(result, NavigableString):
            raise IllegalArgumentsException()

        return result
