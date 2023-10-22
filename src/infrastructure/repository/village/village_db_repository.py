from typing import List

from injector import inject

from src.domain.shared.village import Village
from src.domain.shared.village_repository import VillageRepository
from src.infrastructure.mongodb.village.village_dao import VillageDao
from src.infrastructure.mongodb.village.village_dto import VillageDto
from src.infrastructure.mongodb.village.village_dto_factory import VillageDtoFactory


class VillageDbRepository(VillageRepository):
    @inject
    def __init__(self, dao: VillageDao, factory: VillageDtoFactory):
        self._dao = dao
        self._factory = factory

    def addAll(self, villages: List[Village]) -> None:
        dtos: List[VillageDto] = [self._factory.create(village) for village in villages]
        self._dao.insertAll(dtos)
