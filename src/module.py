from injector import Module

from src.config.mongodb import get_database
from src.crawler import Crawler
from src.domain.latest_crawled.latest_crawled_repository import LatestCrawledRepository
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dao import (
    LatestCrawledDao,
)
from src.infrastructure.repository.latest_crawled.latest_crawled_db_repository import (
    LatestCrawledDbRepository,
)


class BanJinroLogCrawlerModule(Module):
    def configure(self, binder):
        # Facade
        binder.bind(Crawler)

        # Infrastructure
        # - Repository
        binder.bind(LatestCrawledRepository, to=LatestCrawledDbRepository)

        # - MongoDB
        binder.bind(LatestCrawledDao, lambda: LatestCrawledDao(get_database()))
