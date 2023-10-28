from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class UtcDate:
    _value: datetime

    @classmethod
    def now(cls):
        return cls(datetime.now(timezone.utc))

    @classmethod
    def from_epoch_seconds(cls, epoch_seconds: int):
        return cls(datetime.fromtimestamp(epoch_seconds, timezone.utc))

    @classmethod
    def from_timezone_string(
        cls, value: str, format: str, zoneinfo: ZoneInfo = ZoneInfo("UTC")
    ):
        # strptime では local_timezone が利用されるので、timezone のみ replace した後、
        # utc timezone の日付に変換を行っている。
        d: datetime = (
            datetime.strptime(value, format)
            .replace(tzinfo=zoneinfo)
            .astimezone(ZoneInfo("UTC"))
        )

        return cls.from_epoch_seconds(int(d.timestamp()))

    def iso_format(self, timezone: ZoneInfo = ZoneInfo("UTC")) -> str:
        return self._value.astimezone(timezone).strftime('%Y-%m-%dT%H:%M:%SZ')

    def to_epoch_seconds(self) -> int:
        return int(self._value.timestamp())
