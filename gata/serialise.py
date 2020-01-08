from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from typing import Any

from .format import Format
from .utils.is_dataclass_type import is_dataclass_type

ARRAY_TYPES = (list, set)


def serialise(value: Any, source_type) -> Any:
    # List and sets
    origin_type = getattr(source_type, "__origin__", None)
    if origin_type and origin_type in ARRAY_TYPES:
        (arg_type,) = source_type.__args__
        if not arg_type:
            raise ValueError(
                "Cannot serialise generic lists/sets. Please List/Set subtype."
            )

        if value is None:
            return [] if origin_type is list else set()

        if origin_type == list:
            return [serialise(item, arg_type) for item in value]

        return {serialise(item, arg_type) for item in value}

    # Nullables
    if value is None:
        return None

    # Enums
    if isinstance(value, Enum):
        return value.value

    # Dataclass
    if is_dataclass_type(source_type):
        return value.serialise()

    # Strings
    if source_type in (str, int, float, bool):
        return source_type(value)

    # Datetimes
    if source_type is datetime:
        return Format.DATETIME.formatter.extract(value)

    # Dates
    if source_type is date:
        return Format.DATE.formatter.extract(value)

    # Times
    if source_type is time:
        return Format.TIME.formatter.extract(value)

    return value


__all__ = ["serialise"]
