import requests
from injector import inject

from src.config.config import get_config
from src.exceptions.exceptions import ApiRequestException

config = get_config()


class RuruApiUrlFactory:
    URL: str = "https://ruru-jinro.net/{log_number}/{village}.html"

    def create(self, village_number: int) -> str:
        return self.URL.format(
            log_number=self._to_log_number(village_number),
            village=self._to_village_number(village_number),
        )

    def _to_log_number(self, village_number: int) -> str:
        return ""

    def _to_village_number(self, village_number: int) -> str:
        return ""


class RuruApi:
    @inject
    def __init__(self, factory: RuruApiUrlFactory):
        self._factory = factory

    def read(self, village_number: int) -> bytes:
        res = requests.get(
            self._factory.create(village_number),
            timeout=10,
            proxies={"https": config.proxy},
        )

        try:
            res.raise_for_status()
        except Exception as ex:
            raise ApiRequestException(f"api ruru: {village_number}") from ex

        return res.content
