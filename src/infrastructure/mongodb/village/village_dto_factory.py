from typing import List

from bson import ObjectId

from src.domain.shared.village import Village, VillageBans
from src.infrastructure.mongodb.village.village_dto import VillageBansDto, VillageDto


class VillageDtoFactory:
    def create(self, village: Village) -> VillageDto:
        dto: VillageDto = VillageDto(
            _id=ObjectId(),
            villageNumber=village.village_number,
            endDate=village.end_date,
            name=village.name,
            people=village.people,
            cast=village.cast.value,
            bans=self._to_bans(village.bans),
        )
        return dto

    def _to_bans(self, bans: List[VillageBans]) -> List[VillageBansDto]:
        return [
            VillageBansDto(position=ban.position.value, trip=ban.trip) for ban in bans
        ]
