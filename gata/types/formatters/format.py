from enum import Enum
from .base64_formatter import Base64Formatter
from .datetime_formatter import DateTimeFormatter
from .boolean_formatter import BooleanFormatter
from .default_formatter import DefaultFormatter
from .date_formatter import DateFormatter
from .time_formatter import TimeFormatter


class Format(Enum):
    DATETIME = DateTimeFormatter
    DATE = DateFormatter
    TIME = TimeFormatter
    URI = DefaultFormatter
    URL = DefaultFormatter
    EMAIL = DefaultFormatter
    UUID = DefaultFormatter
    HOSTNAME = DefaultFormatter
    IPV4 = DefaultFormatter
    IPV6 = DefaultFormatter
    TRUTHY = BooleanFormatter
    FALSY = BooleanFormatter
    SEMVER = DefaultFormatter
    BYTE = Base64Formatter


__all__ = ["Format"]
