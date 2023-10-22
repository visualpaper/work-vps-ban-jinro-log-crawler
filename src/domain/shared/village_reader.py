from abc import ABC, abstractmethod
from typing import Optional

from src.domain.shared.village import Village


class VillageReader(ABC):
    @abstractmethod
    def read(self, village_number: int) -> Optional[Village]:
        # 村がまだ存在しない場合は None を、
        # 村が存在し、通報対象者がいない場合は village.bans が空を、
        # 村が存在し、通報対象者がいる場合は village.bans が空以外を返却する。
        pass
