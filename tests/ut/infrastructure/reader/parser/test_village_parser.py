from zoneinfo import ZoneInfo

import pytest

from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition
from src.infrastructure.reader.parser.village_parser import VillageParser
from tests.tests_utils import mockdata


class TestVillageParser:
    _api: VillageParser

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._parser = VillageParser()
        yield

    def test_100000(self):
        data = mockdata("ut/infrastructure/reader/parser/100000.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 100000
        assert actual.name == "100000"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2013-03-19T06:54:44Z"
        )
        assert actual.people == 17
        assert actual.cast == VillageCast.A
        assert actual.bans == []

    def test_118145(self):
        data = mockdata("ut/infrastructure/reader/parser/118145.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 118145
        assert actual.name == "チィさんと愉快な仲間たち"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2013-05-04T20:16:32Z"
        )
        assert actual.people == 10
        assert actual.cast == VillageCast.C
        assert actual.bans == []

    def test_188951(self):
        data = mockdata("ut/infrastructure/reader/parser/188951.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 188951
        assert actual.name == "12B"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2014-01-12T00:35:02Z"
        )
        assert actual.people == 12
        assert actual.cast == VillageCast.B
        assert len(actual.bans) == 1
        assert actual.bans[0].position == VillagePosition.MEDIUM
        assert actual.bans[0].trip == "【kari◆wKIIMYcKlx】"

    def test_223279(self):
        data = mockdata("ut/infrastructure/reader/parser/223279.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 223279
        assert actual.name == "１７A！"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2014-07-16T21:19:57Z"
        )
        assert actual.people == 1
        assert actual.cast == VillageCast.A
        assert actual.bans == []

    def test_223280(self):
        data = mockdata("ut/infrastructure/reader/parser/223280.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 223280
        assert actual.name == "廃村"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2014-07-16T21:47:23Z"
        )
        assert actual.people == 2
        assert actual.cast == VillageCast.Z
        assert actual.bans == []

    def test_244433(self):
        data = mockdata("ut/infrastructure/reader/parser/244433.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 244433
        assert actual.name == "はんげ～"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2014-11-09T07:34:58Z"
        )
        assert actual.people == 8
        assert actual.cast == VillageCast.Z
        assert actual.bans == []

    def test_244434(self):
        data = mockdata("ut/infrastructure/reader/parser/244434.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 244434
        assert actual.name == "猫もふわり14D"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2014-11-09T10:32:57Z"
        )
        assert actual.people == 14
        assert actual.cast == VillageCast.D
        assert actual.bans == []

    def test_255121(self):
        data = mockdata("ut/infrastructure/reader/parser/255121.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 255121
        assert actual.name == "ふつうのスカイプ人狼/中辛"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2015-01-10T07:56:51Z"
        )
        assert actual.people == 12
        assert actual.cast == VillageCast.A
        assert actual.bans == []

    def test_255122(self):
        data = mockdata("ut/infrastructure/reader/parser/255122.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 255122
        assert actual.name == "おはよう１１A"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2015-01-10T09:35:40Z"
        )
        assert actual.people == 11
        assert actual.cast == VillageCast.A
        assert actual.bans == []

    def test_299768(self):
        data = mockdata("ut/infrastructure/reader/parser/299768.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 299768
        assert actual.name == "17A普通"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2015-07-31T22:12:51Z"
        )
        assert actual.people == 17
        assert actual.cast == VillageCast.A
        assert actual.bans == []

    def test_346100(self):
        data = mockdata("ut/infrastructure/reader/parser/346100.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 346100
        assert actual.name == "12B"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2016-03-14T23:52:56Z"
        )
        assert actual.people == 12
        assert actual.cast == VillageCast.B
        assert len(actual.bans) == 1
        assert actual.bans[0].position == VillagePosition.VILLAGER
        assert actual.bans[0].trip == "【熊坂学◆xFAcMSgLgT】"

    def test_487441(self):
        data = mockdata("ut/infrastructure/reader/parser/487441.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 487441
        assert actual.name == "【誰歓】17A"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2020-05-16T21:00:31Z"
        )
        assert actual.people == 17
        assert actual.cast == VillageCast.A
        assert len(actual.bans) == 1
        assert actual.bans[0].position == VillagePosition.MASON
        assert actual.bans[0].trip == "【ぱくこ◆LIFQ8ZGQ3b】"

    def test_491562(self):
        data = mockdata("ut/infrastructure/reader/parser/491562.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 491562
        assert actual.name == "CN=HN17A"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2020-08-09T22:29:22Z"
        )
        assert actual.people == 17
        assert actual.cast == VillageCast.A
        assert len(actual.bans) == 1
        assert actual.bans[0].position == VillagePosition.SEER
        assert actual.bans[0].trip == "【柊真雪◆gN3HXC8ego】"

    def test_505930(self):
        data = mockdata("ut/infrastructure/reader/parser/505930.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 505930
        assert actual.name == "宇宙の日ふつう17A"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2023-09-12T21:09:14Z"
        )
        assert actual.people == 4
        assert actual.cast == VillageCast.A
        assert actual.bans == []

    def test_506238(self):
        data = mockdata("ut/infrastructure/reader/parser/506238.html")

        actual = self._parser.parse(data.encode("utf-8"))
        assert actual.village_number == 506238
        assert actual.name == "オールジャンルRP19D猫"
        assert (
            actual.end_date.iso_format(ZoneInfo("Asia/Tokyo")) == "2023-10-28T21:49:01Z"
        )
        assert actual.people == 19
        assert actual.cast == VillageCast.D
        assert actual.bans == []
