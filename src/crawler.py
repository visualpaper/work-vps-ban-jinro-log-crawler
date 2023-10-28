import time

from injector import inject

from src.config.config import get_config
from src.config.logger import get_logger
from src.domain.latest_crawled.latest_crawled_repository import LatestCrawledRepository
from src.domain.shared.village import Village
from src.domain.shared.village_reader import VillageReader
from src.domain.shared.village_repository import VillageRepository

config = get_config()
logger = get_logger()


class Crawler:
    @inject
    def __init__(
        self,
        latest_crawled_repository: LatestCrawledRepository,
        village_repository: VillageRepository,
        village_reader: VillageReader,
    ):
        self._latest_crawled_repository = latest_crawled_repository
        self._village_repository = village_repository
        self._village_reader = village_reader

    def _is_save(self, village: Village) -> bool:
        # 通報対象者がいない場合は記録しない。
        if len(village.bans) == 0:
            return False

        # 通報対象者がいるが、開始前の場合は記録しない。
        if any(ban.position is None for ban in village.bans):
            return False

        # 通報対象者がおり、開始済みだが、8 人未満の場合は記録しない。
        if village.people < 8:
            return False

        return True

    def crawl(self):
        # 最終読み込み村番号を取得する。
        latest_crawle_village_number = self._latest_crawled_repository.read()

        # 指定件数分、読み込みを行う。
        for i in range(config.read_count_limit):
            time.sleep(config.read_wait_seconds)

            village_number = latest_crawle_village_number + (i + 1)

            logger.info("read start - {0}".format(village_number))
            village = self._village_reader.read(village_number)

            # まだ村が存在しない場合、そこで中断する。
            if village is None:
                break

            # 記録しない条件に合致しない場合のみ、記録する。
            if self._is_save(village):
                self._village_repository.add(village)

            # 村が存在する場合、最終読み込み村番号を更新する。
            self._latest_crawled_repository.update(village_number)
