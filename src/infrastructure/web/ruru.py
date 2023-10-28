from typing import Optional

import requests
from injector import inject

from src.config.config import get_config
from src.exceptions.exceptions import ApiRequestException

config = get_config()


class RuruApiUrlFactory:
    URL: str = "https://ruru-jinro.net/log{log_number}/log{number}.html"

    # 1000 ～ 99999 までは log/log99999
    # 100000 ～ 199999 までは log2/log199999
    # 200000 ～ 299999 までは log3/log299999
    # ... のように続いていく。
    SEPARATE_NUMBER: int = 100000

    def create(self, village_number: int) -> str:
        return self.URL.format(
            log_number=self._to_log_number(village_number),
            number=village_number,
        )

    def _to_log_number(self, village_number: int) -> str:
        if village_number < self.SEPARATE_NUMBER:
            return ""

        return str((village_number // self.SEPARATE_NUMBER) + 1)


class RuruApi:
    @inject
    def __init__(self, factory: RuruApiUrlFactory):
        self._factory = factory

    def read(self, village_number: int) -> Optional[bytes]:
        res = requests.get(
            self._factory.create(village_number),
            timeout=10,
            proxies={"https": config.proxy},
        )

        if res.status_code == 404:
            return None

        try:
            res.raise_for_status()
        except Exception as ex:
            raise ApiRequestException(f"api ruru: {village_number}") from ex

        return res.content
