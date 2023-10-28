import pytest

from infrastructure.web.ruru import RuruApiUrlFactory


class TestRuruApiUrlFactory:
    _sut: RuruApiUrlFactory

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._sut = RuruApiUrlFactory()
        yield

    @pytest.mark.parametrize(
        "actual, expected",
        [
            (1000, "https://ruru-jinro.net/log/log1000.html"),
            (9999, "https://ruru-jinro.net/log/log9999.html"),
            (99999, "https://ruru-jinro.net/log/log99999.html"),
            (100000, "https://ruru-jinro.net/log2/log100000.html"),
            (100001, "https://ruru-jinro.net/log2/log100001.html"),
            (199999, "https://ruru-jinro.net/log2/log199999.html"),
            (200000, "https://ruru-jinro.net/log3/log200000.html"),
            (200001, "https://ruru-jinro.net/log3/log200001.html"),
            (999999, "https://ruru-jinro.net/log10/log999999.html"),
            (1000000, "https://ruru-jinro.net/log11/log1000000.html"),
        ],
    )
    def test_of(self, actual, expected):
        assert self._sut.create(actual) == expected
