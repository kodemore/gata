from collections.abc import Sequence as ABCSequence
from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from functools import partial
from inspect import isclass
from numbers import Integral
from numbers import Rational
from numbers import Real
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Set
from typing import Union

from gata.errors import TypeMapError
from gata.utils.is_dataclass_type import is_dataclass_type
from gata.validators.validate_any import validate_any
from gata.validators.validate_array import validate_array
from gata.validators.validate_boolean import validate_boolean
from gata.validators.validate_date import validate_date
from gata.validators.validate_datetime import validate_datetime
from gata.validators.validate_enum import validate_enum
from gata.validators.validate_integer import validate_integer
from gata.validators.validate_nullable import validate_nullable
from gata.validators.validate_number import validate_number
from gata.validators.validate_string import validate_string
from gata.validators.validate_time import validate_time

TYPE_MAPPING = {
    Any: lambda x: None,
    Set: partial(validate_array, unique=True),
    bool: validate_boolean,
    date: validate_date,
    datetime: validate_datetime,
    time: validate_time,
    int: validate_integer,
    Integral: validate_integer,
    Iterable: validate_array,
    Real: validate_number,
    Rational: validate_number,
    float: validate_number,
    str: validate_string,
}


def map_list(origin_type) -> Callable:
    (value_type,) = origin_type.__args__

    return partial(validate_array, items=map_type_to_validator(value_type))


def map_set(origin_type) -> Callable:
    (value_type,) = origin_type.__args__

    return partial(validate_array, items=map_type_to_validator(value_type), unique=True)


def map_union(origin_type) -> Callable:
    allowed_types = origin_type.__args__

    # Optional type support
    if len(allowed_types) == 2 and isinstance(None, allowed_types[1]):
        return partial(
            validate_nullable, validator=map_type_to_validator(allowed_types[0])
        )

    # Union type support
    validators = [map_type_to_validator(subtype) for subtype in allowed_types]
    return partial(validate_any, validators=validators)


ORIGIN_TO_HANDLER_MAP = {
    set: map_set,
    list: map_list,
    ABCSequence: map_list,
    Union: map_union,
}


def map_type_to_validator(python_type) -> Callable[..., bool]:

    # Simple map one to one
    if python_type in TYPE_MAPPING:
        return TYPE_MAPPING[python_type]

    # Map enums
    if isclass(python_type) and issubclass(python_type, Enum):
        return partial(validate_enum, enum=python_type)

    # Map complex type
    origin_type = getattr(python_type, "__origin__", None)
    if origin_type in ORIGIN_TO_HANDLER_MAP:
        return ORIGIN_TO_HANDLER_MAP[origin_type](python_type)

    if is_dataclass_type(python_type):
        return python_type.validate

    # Optional types
    if isinstance(None, python_type):
        pass

    raise TypeMapError(f"Cannot map {python_type} in dataclass.")


__all__ = ["map_type_to_validator"]
