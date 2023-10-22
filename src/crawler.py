from injector import inject

from src.domain.latest_crawled.latest_crawled_repository import LatestCrawledRepository


class Crawler:
    @inject
    def __init__(self, latest_crawled_repository: LatestCrawledRepository):
        self._latest_crawled_repository = latest_crawled_repository

    def crawl(self):
        print(self._latest_crawled_repository.read())
        # 読み込み済み村番号を取得する
        # latestCrawledRepository = injector.get(LatestCrawledRepository)
        # latestCrawledVillageNumber = latestCrawledRepository.getLatest()
