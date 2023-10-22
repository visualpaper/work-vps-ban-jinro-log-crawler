from utc_date import UtcDate


class TestUtcDate:
    def test_normal(self):
        d: UtcDate = UtcDate.from_epoch_seconds(1697970899)

        assert d.to_epoch_seconds() == 1697970899
        assert d.iso_format() == "2023-10-22T10:34:59Z"
