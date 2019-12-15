from collections.abc import Sequence as ABCSequence
from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum as enumEnum
from inspect import isclass
from numbers import Integral
from numbers import Rational
from numbers import Real
from typing import Any as TypingAny
from typing import Iterable
from typing import List
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

from gata.errors import TypeMapError
from gata.types.any import Any
from gata.types.any_of import AnyOf
from gata.types.array import Array
from gata.types.boolean import Boolean
from gata.types.enum import Enum
from gata.types.integer import Integer
from gata.types.null import Null
from gata.types.number import Number
from gata.types.string import Format
from gata.types.string import String
from gata.types.type import Type
from .is_dataclass import is_dataclass

TYPE_MAPPING = {
    TypingAny: Any,
    list: Array,
    List: Array,
    Tuple: Array,
    Sequence: Array,
    Set: Array(unique_items=True),
    set: Array(unique_items=True),
    tuple: Array,
    bool: Boolean,
    date: String(string_format=Format.DATE),
    datetime: String(string_format=Format.DATETIME),
    time: String(string_format=Format.TIME),
    int: Integer,
    Integral: Integer,
    Iterable: Array,
    Real: Number,
    Rational: Number,
    float: Number,
    str: String,
}


def map_list(origin_type):
    (value_type,) = origin_type.__args__

    return Array(items=map_type(value_type))


def map_union(origin_type) -> Type:
    allowed_types = origin_type.__args__

    # Optional type support
    if len(allowed_types) == 2 and isinstance(None, allowed_types[1]):
        mapped_type = map_type(allowed_types[0])
        mapped_type.nullable = True
        return mapped_type

    # Union type support
    mapped_subtypes = [map_type(subtype) for subtype in allowed_types]
    return AnyOf[mapped_subtypes]


ORIGIN_TO_HANDLER_MAP = {
    list: map_list,
    ABCSequence: map_list,
    Union: map_union,
}


def map_type(python_type) -> Type:

    # Simple map one to one
    if python_type in TYPE_MAPPING:
        return TYPE_MAPPING[python_type]

    # Map enums
    if isclass(python_type) and issubclass(python_type, enumEnum):
        values = [item.value for item in list(python_type)]
        result = Enum[values]
        result.target = python_type

        return result

    # Map complex type
    origin_type = getattr(python_type, "__origin__", None)
    if origin_type in ORIGIN_TO_HANDLER_MAP:
        return ORIGIN_TO_HANDLER_MAP[origin_type](python_type)

    # Dataclasses
    if is_dataclass(python_type):
        return python_type

    # Gata types
    if isinstance(python_type, Type):
        return python_type

    # Optional types
    if isinstance(None, python_type):
        return Null

    raise TypeMapError(f"Cannot map {python_type} in dataclass.")


__all__ = ["map_type"]
