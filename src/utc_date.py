from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class UtcDate:
    _now: datetime

    @classmethod
    def now(cls):
        return cls(datetime.now(timezone.utc))

    def iso_format(self) -> str:
        return self._now.isoformat()
