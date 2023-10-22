from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class UtcDate:
    _value: datetime

    @classmethod
    def now(cls):
        return cls(datetime.now(timezone.utc))

    @classmethod
    def from_epoch_seconds(cls, epoch_seconds: int):
        return cls(datetime.fromtimestamp(epoch_seconds, timezone.utc))

    def iso_format(self) -> str:
        return self._value.strftime('%Y-%m-%dT%H:%M:%SZ')

    def to_epoch_seconds(self) -> int:
        return int(self._value.timestamp())
