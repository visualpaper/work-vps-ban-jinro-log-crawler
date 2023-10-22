import pytest

from tests.tests_utils import mockdata
from src.infrastructure.reader.parser.village_parser import VillageParser


class TestVillageParser:
    _api: VillageParser

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._parser = VillageParser()
        yield

    def test_1000(self):
        data = mockdata("ut/infrastructure/reader/parser/1000.html")

        actual = self._parser.parse(data.encode("utf-8"))
