from injector import Injector

from src.config.config import get_config
from src.config.logger import get_logger
from src.config.mongodb import close_mongo_connection, connect_to_mongo
from src.crawler import Crawler
from src.module import BanJinroLogCrawlerModule
from src.utc_date import UtcDate

injector = Injector([BanJinroLogCrawlerModule()])
config = get_config()
logger = get_logger()


# エントリポイント
if __name__ == "__main__":
    logger.info("start - {0}".format(UtcDate.now().iso_format()))

    connect_to_mongo(config)
    crawler = injector.get(Crawler)
    crawler.crawl()
    close_mongo_connection()

    logger.info("end - {0}".format(UtcDate.now().iso_format()))
