from typing import Optional

import mongomock
import pytest
from bson import ObjectId
from pymongo.collection import Collection

from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_position import VillagePosition
from src.infrastructure.mongodb.village.village_dao import VillageDao
from src.infrastructure.mongodb.village.village_dto import VillageBansDto, VillageDto
from utc_date import UtcDate


class TestVillageDao:
    _dao: VillageDao
    _collection: Collection

    @pytest.fixture(autouse=True)
    def fixture(self):
        client = mongomock.MongoClient()
        db = client["db"]
        self._dao = VillageDao(db)
        self._collection = client["db"]["td_village"]
        yield
        client.drop_database("db")

    def test_normal(self):
        dto1: VillageDto = VillageDto(
            _id=ObjectId(),
            villageNumber=1,
            endDate=UtcDate.now().to_epoch_seconds(),
            name="aaa",
            people=10,
            cast=VillageCast.A.value,
            bans=[VillageBansDto(position=VillagePosition.WOLF.value, trip="aaa")],
        )
        dto2: VillageDto = VillageDto(
            _id=ObjectId(),
            villageNumber=1,
            endDate=UtcDate.now().to_epoch_seconds(),
            name="bbb",
            people=11,
            cast=VillageCast.B.value,
            bans=[
                VillageBansDto(position=VillagePosition.APOSTATE.value, trip="cc"),
                VillageBansDto(position=VillagePosition.CAT.value, trip="dd"),
            ],
        )
        self._dao.insertAll([dto1, dto2])

        expected1: Optional[VillageDto] = self._collection.find_one(
            {'_id': dto1["_id"]}
        )
        assert expected1 is not None
        assert expected1["villageNumber"] == dto1["villageNumber"]
        assert expected1["endDate"] == dto1["endDate"]
        assert expected1["name"] == dto1["name"]
        assert expected1["people"] == dto1["people"]
        assert expected1["cast"] == dto1["cast"]
        assert len(expected1["bans"]) == len(dto1["bans"])
        assert expected1["bans"][0]["position"] == dto1["bans"][0]["position"]
        assert expected1["bans"][0]["trip"] == dto1["bans"][0]["trip"]

        expected2: Optional[VillageDto] = self._collection.find_one(
            {'_id': dto2["_id"]}
        )
        assert expected2 is not None
        assert expected2 is not None
        assert expected2["villageNumber"] == dto2["villageNumber"]
        assert expected2["endDate"] == dto2["endDate"]
        assert expected2["name"] == dto2["name"]
        assert expected2["people"] == dto2["people"]
        assert expected2["cast"] == dto2["cast"]
        assert len(expected2["bans"]) == len(dto2["bans"])
        assert expected2["bans"][0]["position"] == dto2["bans"][0]["position"]
        assert expected2["bans"][0]["trip"] == dto2["bans"][0]["trip"]
        assert expected2["bans"][1]["position"] == dto2["bans"][1]["position"]
        assert expected2["bans"][1]["trip"] == dto2["bans"][1]["trip"]
