from datetime import date
from datetime import datetime as python_datetime
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
from collections.abc import Sequence as ABCSequence

from gata.errors import TypeMapError
from .any import Any
from .array import Array
from .boolean import Boolean
from .datetime import Date
from .datetime import DateTime
from .datetime import Time
from .enum import Enum
from .formatters.format import Format
from .integer import Integer
from .number import Number
from .object import Object
from .string import String
from .type import Type

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
    date: Date,
    python_datetime: DateTime,
    time: Time,
    int: Integer,
    Integral: Integer,
    Iterable: Array,
    Real: Number,
    Rational: Number,
    float: Number,
    str: String,
}


def map_list(origin_type) -> None:
    value_type, = origin_type.__args__

    return Array(items=map_type(value_type))


ORIGIN_TO_HANDLER_MAP = {
    list: map_list,
    ABCSequence: map_list,
}


def map_type(python_type) -> Type:
    if python_type in TYPE_MAPPING:
        return TYPE_MAPPING[python_type]

    if isclass(python_type) and issubclass(python_type, enumEnum):
        values = [item.value for item in list(python_type)]
        return Enum(*values)

    origin_type = getattr(python_type, "__origin__", None)

    if origin_type in ORIGIN_TO_HANDLER_MAP:
        return ORIGIN_TO_HANDLER_MAP[origin_type](python_type)

    raise TypeMapError(f"Cannot map {python_type} in dataclass.")


__all__ = [
    "Any",
    "Array",
    "Boolean",
    "Date",
    "DateTime",
    "Enum",
    "Format",
    "Integer",
    "Number",
    "Object",
    "String",
    "Time",
    "Type",

    "map_type",
]
