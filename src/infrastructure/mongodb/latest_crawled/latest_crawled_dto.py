from typing import TypedDict

from bson import ObjectId


class LatestCrawledDto(TypedDict):
    _id: ObjectId
    value: int
