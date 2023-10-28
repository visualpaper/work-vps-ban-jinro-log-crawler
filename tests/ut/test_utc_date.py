from zoneinfo import ZoneInfo

from src.utc_date import UtcDate


class TestUtcDate:
    def test_from_epoch_seconds(self):
        # 日本時間 2023-10-22T19:34:59Z
        d: UtcDate = UtcDate.from_epoch_seconds(1697970899)

        assert d.to_epoch_seconds() == 1697970899
        assert d.iso_format() == "2023-10-22T10:34:59Z"
        assert d.iso_format(ZoneInfo("Asia/Tokyo")) == "2023-10-22T19:34:59Z"

    def test_from_string(self):
        d: UtcDate = UtcDate.from_timezone_string(
            "2023-10-22T19:34:59Z", "%Y-%m-%dT%H:%M:%SZ", ZoneInfo("Asia/Tokyo")
        )

        assert d.to_epoch_seconds() == 1697970899
        assert d.iso_format() == "2023-10-22T10:34:59Z"
        assert d.iso_format(ZoneInfo("Asia/Tokyo")) == "2023-10-22T19:34:59Z"
