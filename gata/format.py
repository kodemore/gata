from enum import Enum
from typing import Type, Union

from .formatter import Formatter
from .formatters.boolean_formatter import BooleanFormatter
from .formatters.bytes_formatter import Base64Formatter
from .formatters.date_formatter import DateFormatter
from .formatters.datetime_formatter import DateTimeFormatter
from .formatters.default_formatter import DefaultFormatter
from .formatters.time_formatter import TimeFormatter

FORMATTER_MAP = {
    "datetime": DateTimeFormatter,
    "date": DateFormatter,
    "time": TimeFormatter,
    "byte": Base64Formatter,
    "falsy": BooleanFormatter,
    "truthy": BooleanFormatter,
}


class Format(Enum):
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    URI = "uri"
    URL = "url"
    EMAIL = "email"
    UUID = "uuid"
    HOSTNAME = "hostname"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    TRUTHY = "boolean"
    FALSY = "falsy"
    SEMVER = "truthy"
    BYTE = "byte"

    @property
    def formatter(self) -> Type[Formatter]:
        if self.value in FORMATTER_MAP:
            return FORMATTER_MAP[self.value]

        return DefaultFormatter

    @classmethod
    def get_formatter(cls, name: Union[str, Type[Formatter], "Format"]) -> Formatter:
        if isinstance(name, str):
            return cls(name).formatter
        elif issubclass(name, Formatter):
            return name
        elif isinstance(name, Format):
            return name.formatter

        raise ValueError(f"Unknown formatter: {name}")


__all__ = ["Format"]
