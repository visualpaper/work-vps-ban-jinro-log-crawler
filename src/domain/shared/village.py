from dataclasses import dataclass
from typing import List

from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition
from utc_date import UtcDate


@dataclass(frozen=True)
class VillageBans:
    position: VillagePosition
    trip: str


@dataclass(frozen=True)
class Village:
    village_number: int
    end_date: UtcDate
    name: str
    people: int
    cast: VillageCast
    bans: List[VillageBans]
