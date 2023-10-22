from dataclasses import dataclass
from datetime import date
from typing import List

from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition


@dataclass(frozen=True)
class VillageBans:
    position: VillagePosition
    trip: str


@dataclass(frozen=True)
class Village:
    village_number: int
    end_date: date
    name: str
    people: int
    cast: VillageCast
    bans: List[VillageBans]
