import pytest

from src.domain.shared.village import Village, VillageBans
from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition
from src.infrastructure.mongodb.village.village_dto import VillageDto
from src.infrastructure.mongodb.village.village_dto_factory import VillageDtoFactory
from src.utc_date import UtcDate


class TestVillageDtoFactory:
    _sut: VillageDtoFactory

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._sut = VillageDtoFactory()
        yield

    def test_one(self):
        actual: Village = Village(
            1,
            UtcDate.now(),
            "aaa",
            10,
            VillageCast.A,
            [VillageBans(VillagePosition.APOSTATE, "cc")],
        )
        expected: VillageDto = self._sut.create(actual)

        assert actual.village_number == expected["villageNumber"]
        assert (
            actual.end_date.iso_format()
            == UtcDate.from_epoch_seconds(expected["endDate"]).iso_format()
        )
        assert actual.name == expected["name"]
        assert actual.people == expected["people"]
        assert actual.cast.value == expected["cast"]
        assert actual.bans[0].position.value == expected["bans"][0]["position"]
        assert actual.bans[0].trip == expected["bans"][0]["trip"]

    def test_many(self):
        actual: Village = Village(
            1,
            UtcDate.now(),
            "aaa",
            10,
            VillageCast.A,
            [
                VillageBans(VillagePosition.APOSTATE, "cc"),
                VillageBans(VillagePosition.WOLF, "dd"),
            ],
        )
        expected: VillageDto = self._sut.create(actual)

        assert actual.village_number == expected["villageNumber"]
        assert (
            actual.end_date.iso_format()
            == UtcDate.from_epoch_seconds(expected["endDate"]).iso_format()
        )
        assert actual.name == expected["name"]
        assert actual.people == expected["people"]
        assert actual.cast.value == expected["cast"]
        assert actual.bans[0].position.value == expected["bans"][0]["position"]
        assert actual.bans[0].trip == expected["bans"][0]["trip"]
        assert actual.bans[1].position.value == expected["bans"][1]["position"]
        assert actual.bans[1].trip == expected["bans"][1]["trip"]
