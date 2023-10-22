from injector import Module

from src.config.mongodb import get_database
from src.crawler import Crawler
from src.domain.latest_crawled.latest_crawled_repository import LatestCrawledRepository
from src.domain.shared.village_reader import VillageReader
from src.domain.shared.village_repository import VillageRepository
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dao import (
    LatestCrawledDao,
)
from src.infrastructure.mongodb.village.village_dao import VillageDao
from src.infrastructure.mongodb.village.village_dto_factory import VillageDtoFactory
from src.infrastructure.reader.parser.village_parser import VillageParser
from src.infrastructure.reader.village_web_reader import VillageWebReader
from src.infrastructure.repository.latest_crawled.latest_crawled_db_repository import (
    LatestCrawledDbRepository,
)
from src.infrastructure.repository.village.village_db_repository import (
    VillageDbRepository,
)
from src.infrastructure.web.ruru import RuruApi, RuruApiUrlFactory


class BanJinroLogCrawlerModule(Module):
    def configure(self, binder):
        # Facade
        binder.bind(Crawler)

        # Infrastructure
        # - Reader
        binder.bind(VillageReader, to=VillageWebReader)

        # - Web
        binder.bind(RuruApi)
        binder.bind(RuruApiUrlFactory)
        binder.bind(VillageParser)

        # - Repository
        binder.bind(VillageRepository, to=VillageDbRepository)
        binder.bind(LatestCrawledRepository, to=LatestCrawledDbRepository)

        # - MongoDB
        db = get_database()
        binder.bind(VillageDao, lambda: VillageDao(db))
        binder.bind(VillageDtoFactory)
        binder.bind(LatestCrawledDao, lambda: LatestCrawledDao(db))
