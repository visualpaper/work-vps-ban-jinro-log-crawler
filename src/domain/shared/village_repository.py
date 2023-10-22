from abc import ABC, abstractmethod
from typing import List

from src.domain.shared.village import Village


class VillageRepository(ABC):
    @abstractmethod
    def addAll(self, villages: List[Village]) -> None:
        pass
