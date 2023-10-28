from typing import Optional

from injector import inject

from src.domain.shared.village import Village
from src.domain.shared.village_reader import VillageReader
from src.exceptions.exceptions import (
    ApiRequestException,
    IllegalStateException,
    ParserException,
    VillageReadWriteException,
)
from src.infrastructure.reader.parser.village_parser import VillageParser
from src.infrastructure.web.ruru import RuruApi


class VillageWebReader(VillageReader):
    @inject
    def __init__(self, api: RuruApi, parser: VillageParser):
        self._api = api
        self._parser = parser

    def read(self, village_number: int) -> Optional[Village]:
        try:
            content = self._api.read(village_number)
            if content is None:
                return None

            return self._parser.parse(content)
        except ApiRequestException as ex:
            raise VillageReadWriteException(f'read village: {village_number}') from ex
        except ParserException as ex:
            raise IllegalStateException(f'parse village: {village_number}') from ex
