from datetime import time
from datetime import timedelta
from datetime import timezone
import re
from typing import Any

from .formatter import Formatter

_ISO_8601_TIME_REGEX = re.compile(
    r"^(?P<time>[0-2]\d:?[0-5]\d:?[0-5]\d|23:59:60|235960)(?P<microseconds>\.\d+)?(?P<tzpart>z|[+-]\d{2}:\d{2})?$",
    re.I,
)


class TimeFormatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        if not _ISO_8601_TIME_REGEX.match(value):
            raise ValueError(
                f"Passed value {value} cannot be formatted into ISO 8601 time."
            )
        parts = _ISO_8601_TIME_REGEX.fullmatch(value)
        time_parts = parts.group("time")  # type: ignore
        if ":" in time_parts:
            time_parts = time_parts.split(":")
        else:
            time_parts = list(map("".join, zip(*[iter(time_parts)] * 2)))

        microseconds = parts.group("microseconds")  # type: ignore
        if microseconds is not None:
            microseconds = int(microseconds[1:])
        else:
            microseconds = 0

        tz_part = parts.group("tzpart")  # type: ignore
        if tz_part and tz_part.lower() != "z":
            sign = 1 if tz_part[0] == "+" else -1
            hours, minutes = tz_part[1:].split(":")
            offset = timezone(
                timedelta(hours=int(hours) * sign, minutes=int(minutes) * sign)
            )
        elif tz_part and tz_part.lower() == "z":
            offset = timezone.utc
        else:
            offset = None  # type: ignore

        return time(
            hour=int(time_parts[0]),
            minute=int(time_parts[1]),
            second=int(time_parts[2]),
            microsecond=microseconds,
            tzinfo=offset,
        )

    @classmethod
    def extract(cls, value: time) -> str:
        return value.isoformat()


__all__ = ["TimeFormatter"]
