import pytest

from src.domain.shared.village_position import VillagePosition
from src.exceptions.exceptions import IllegalArgumentsException


class TestVillagePosition:
    @pytest.mark.parametrize(
        "actual",
        [(""), ("a"), (None)],
    )
    def test_of_error(self, actual):
        with pytest.raises(IllegalArgumentsException):
            VillagePosition.of(actual)

    @pytest.mark.parametrize(
        "actual, expected",
        [
            ("人狼", VillagePosition.WOLF),
            ("狂信者", VillagePosition.FANATIC),
            ("狂人", VillagePosition.MADMAN),
            ("妖狐", VillagePosition.FOX),
            ("背徳者", VillagePosition.APOSTATE),
            ("占い師", VillagePosition.SEER),
            ("霊能", VillagePosition.MEDIUM),
            ("狩人", VillagePosition.HUNTER),
            ("猫又", VillagePosition.CAT),
            ("共有", VillagePosition.MASON),
            ("村人", VillagePosition.VILLAGER),
        ],
    )
    def test_of(self, actual, expected):
        assert VillagePosition.of(actual) is expected
