from datetime import datetime
from typing import List

from injector import inject

from src.config.config import get_config
from src.domain.latest_crawled.latest_crawled_repository import LatestCrawledRepository
from src.domain.shared.village import Village
from src.domain.shared.village_cast import VillageCast
from src.domain.shared.village_repository import VillageRepository

config = get_config()


class Crawler:
    @inject
    def __init__(
        self,
        latest_crawled_repository: LatestCrawledRepository,
        village_repository: VillageRepository,
    ):
        self._latest_crawled_repository = latest_crawled_repository
        self._village_repository = village_repository

    def crawl(self):
        villages: List[Village] = []

        latest_crawle_village_number = self._latest_crawled_repository.read()
        for i in range(config.read_count_limit):
            villages.append(self._crawl(latest_crawle_village_number + (i + 1)))

        self._village_repository.addAll(villages)

    def _crawl(self, village_number: int) -> Village:
        return Village(1, datetime.now(), "aaa", 10, VillageCast.A, [])
