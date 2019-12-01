from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from .formatter import Formatter
import re

_ISO_8601_DATETIME_REGEX = re.compile(
    r"^(\d{4})-?([0-1]\d)-?([0-3]\d)[t\s]?([0-2]\d:?[0-5]\d:?[0-5]\d|23:59:60|235960)(\.\d+)?(z|[+-]\d{2}:\d{2})?$",
    re.I,
)


class DateTimeFormatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        if not _ISO_8601_DATETIME_REGEX.match(value):
            raise ValueError(
                f"Passed value {value} cannot be formatted to valid ISO 8601 datetime."
            )
        parts = _ISO_8601_DATETIME_REGEX.findall(value)[0]
        time = parts[3]
        if ":" in time:
            time = time.split(":")
        else:
            time = list(map("".join, zip(*[iter(time)] * 2)))

        if parts[5] and parts[5].lower() != "z":
            sign = 1 if parts[5][0] == "+" else -1
            hours, minutes = parts[5][1:].split(":")
            offset = timezone(
                timedelta(hours=int(hours) * sign, minutes=int(minutes) * sign)
            )
        elif parts[5] and parts[5].lower() == "z":
            offset = timezone.utc
        else:
            offset = None  # type: ignore

        return datetime(
            year=int(parts[0]),
            month=int(parts[1]),
            day=int(parts[2]),
            hour=int(time[0]),
            minute=int(time[1]),
            second=int(time[2]),
            tzinfo=offset,
        )

    @classmethod
    def extract(cls, value: datetime) -> str:
        return value.isoformat()


__all__ = ["DateTimeFormatter"]
