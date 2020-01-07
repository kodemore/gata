from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from inspect import isclass
from typing import Any

from .format import Format
from .utils.is_dataclass_type import is_dataclass_type

ARRAY_TYPES = (list, set)


def unserialise(value: Any, target_type, meta: dict = {}) -> Any:

    # Enums
    if isclass(target_type) and issubclass(target_type, Enum):
        return target_type(value)

    # Dataclass
    if is_dataclass_type(target_type):
        if not isinstance(value, dict):
            raise ValueError(
                f"Cannot unserialise value of type {type(value)} to {target_type}."
            )
        return target_type.unserialise(value)

    # List and sets
    origin_type = getattr(target_type, "__origin__", None)
    if origin_type and origin_type in ARRAY_TYPES:
        (arg_type,) = target_type.__args__
        if not arg_type:
            raise ValueError(
                "Cannot unserialise generic lists/sets. Please List/Set subtype."
            )

        if origin_type == list:
            return [
                unserialise(item, arg_type, meta["items"] if "items" in meta else {})
                for item in value
            ]

        return (
            unserialise(item, arg_type, meta["items"] if "items" in meta else {})
            for item in value
        )

    # Strings
    if target_type is str:
        if "format" in meta:
            formatter = Format.get_formatter(meta["format"])
            return formatter.hydrate(value)

        return value

    # Datetimes
    if target_type is datetime:
        return Format.DATETIME.formatter.hydrate(value)

    # Dates
    if target_type is date:
        return Format.DATE.formatter.hydrate(value)

    # Times
    if target_type is time:
        return Format.TIME.formatter.hydrate(value)

    # Primitives
    if target_type in (int, float, bool):
        return target_type(value)

    return value
