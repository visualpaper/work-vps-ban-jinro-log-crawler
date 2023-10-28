from enum import Enum

from src.exceptions.exceptions import IllegalArgumentsException


class VillagePosition(Enum):
    WOLF = "人狼"
    FANATIC = "狂信者"
    MADMAN = "狂人"
    FOX = "妖狐"
    APOSTATE = "背徳者"
    SEER = "占い師"
    MEDIUM = "霊能"
    HUNTER = "狩人"
    CAT = "猫又"
    MASON = "共有"
    VILLAGER = "村人"

    @classmethod
    def of(cls, value):
        for t in VillagePosition:
            if t.value == value:
                return t

        raise IllegalArgumentsException()
