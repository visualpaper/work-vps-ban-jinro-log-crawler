import pytest
from bson import ObjectId
from pytest_mock.plugin import MockerFixture

from src.exceptions.exceptions import LatestCrawledReadWriteException
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dao import (
    LatestCrawledDao,
)
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dto import (
    LatestCrawledDto,
)
from src.infrastructure.repository.latest_crawled.latest_crawled_db_repository import (
    LatestCrawledDbRepository,
)


class TestLatestCrawledDbRepository:
    _repository: LatestCrawledDbRepository
    _dao_mock: LatestCrawledDao

    @pytest.fixture(autouse=True)
    def fixture(self, mocker: MockerFixture):
        self._dao_mock = mocker.MagicMock()
        self._repository = LatestCrawledDbRepository(self._dao_mock)
        yield

    def test_read(self, mocker: MockerFixture):
        latest_crawled: int = 1

        mocker.patch.object(
            self._dao_mock,
            'read',
            return_value=LatestCrawledDto(_id=ObjectId(), value=latest_crawled),
        )
        assert self._repository.read() == latest_crawled

    def test_read_error(self, mocker: MockerFixture):
        mocker.patch.object(self._dao_mock, 'read', return_value=None)

        with pytest.raises(LatestCrawledReadWriteException):
            self._repository.read()

    def test_update(self, mocker: MockerFixture):
        latest_crawled: int = 1

        mocker.patch.object(
            self._dao_mock,
            'read',
            return_value=LatestCrawledDto(_id=ObjectId(), value=latest_crawled),
        )
        self._repository.update(2)

    def test_update_error(self, mocker: MockerFixture):
        mocker.patch.object(self._dao_mock, 'read', return_value=None)

        with pytest.raises(LatestCrawledReadWriteException):
            self._repository.update(2)
