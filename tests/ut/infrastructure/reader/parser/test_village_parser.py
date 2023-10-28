from zoneinfo import ZoneInfo

import pytest

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
