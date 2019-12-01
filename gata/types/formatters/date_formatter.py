import re
from datetime import date
from typing import Any

from .formatter import Formatter


_ISO_8601_DATE_REGEX = re.compile(r"^(\d{4})-?([0-1]\d)-?([0-3]\d)$", re.I)


class DateFormatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        if not _ISO_8601_DATE_REGEX.match(value):
            raise ValueError(
                f"Passed value {value} cannot be formatted into valid ISO 8601 date."
            )
        parts = _ISO_8601_DATE_REGEX.findall(value)[0]

        return date(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))

    @classmethod
    def extract(cls, value: date) -> str:
        return value.isoformat()


__all__ = ["DateFormatter"]
