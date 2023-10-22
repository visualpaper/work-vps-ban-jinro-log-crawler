from abc import ABC, abstractmethod


class LatestCrawledRepository(ABC):
    @abstractmethod
    def read(self) -> int:
        pass

    @abstractmethod
    def update(self, value: int) -> None:
        pass
