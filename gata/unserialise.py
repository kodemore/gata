from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from inspect import isclass
from typing import Any
from typing import Type
from typing import TypeVar

from .format import Format
from .utils.is_dataclass_type import is_dataclass_type

ARRAY_TYPES = (list, set)

T = TypeVar('T')


def _unserialise_dataclass(value: dict, target_type: Type[T]) -> T:
    if not isinstance(value, dict):
        raise ValueError(
            f"Cannot unserialise value of type {type(value)} to {target_type}."
        )
    return target_type.unserialise(value)  # type: ignore


def _unserialise_list(value, target_type, meta: dict) -> list:
    (arg_type,) = target_type.__args__
    if not arg_type:
        raise ValueError(
            "Cannot unserialise generic lists/sets. Please List/Set subtype."
        )

    return [
        unserialise(item, arg_type, meta["items"] if "items" in meta else {})
        for item in value
    ]


def _unserialise_set(value, target_type, meta: dict) -> set:
    (arg_type,) = target_type.__args__
    if not arg_type:
        raise ValueError(
            "Cannot unserialise generic lists/sets. Please List/Set subtype."
        )

    return set(
        unserialise(item, arg_type, meta["items"] if "items" in meta else {})
        for item in value
    )


def _unserialise_string(value, target_type, meta) -> Any:
    if "format" in meta:
        formatter = Format.get_formatter(meta["format"])
        return formatter.hydrate(value)

    return value


def unserialise(value: Any, target_type, meta: dict = {}) -> Any:
    # Enums
    if isclass(target_type) and issubclass(target_type, Enum):
        return target_type(value)

    # Dataclass
    if is_dataclass_type(target_type):
        return _unserialise_dataclass(value, target_type)

    # List and sets
    origin_type = getattr(target_type, "__origin__", None)
    if origin_type and origin_type in ARRAY_TYPES:
        if origin_type == list:
            return _unserialise_list(value, target_type, meta)
        else:
            return _unserialise_set(value, target_type, meta)

    # Strings
    if target_type is str:
        return _unserialise_string(value, target_type, meta)

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


__all__ = ["unserialise"]
