from base64 import b64decode
from dataclasses import is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from inspect import isclass
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Dict, FrozenSet, List, Set, Tuple, Union
from uuid import UUID

from typing_extensions import Literal

from gata.errors import DeserialisationError
from gata.typing import SerialisableType
from gata.utils import (
    is_typed_dict,
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_time_string,
)


def deserialise_datetype(value: Union[str, date]) -> date:
    if isinstance(value, date):
        return value

    return parse_iso_date_string(value)


def deserialise_datetime_type(value: Union[str, date]) -> datetime:
    if isinstance(value, datetime):
        return value

    return parse_iso_datetime_string(value)  # type: ignore


def deserialise_time_type(value: Union[str, date]) -> time:
    if isinstance(value, time):
        return value

    return parse_iso_time_string(value)  # type: ignore


TYPE_DECODERS = {
    IPv4Address: IPv4Address,
    IPv6Address: IPv6Address,
    UUID: UUID,
    datetime: deserialise_datetime_type,
    date: deserialise_datetype,
    time: deserialise_time_type,
    bool: bool,
    int: int,
    float: float,
    str: str,
    bytes: b64decode,
    Decimal: Decimal,
}


def deserialise_tuple(value: Tuple[Any, ...], subtypes: List[Any]) -> Tuple[Any, ...]:
    if value is None:
        return tuple()

    if not subtypes:
        raise DeserialisationError(
            "Cannot deserialise generic tuples, please ensure subtype in tuple declaration."
        )
    result = []
    for index in range(len(subtypes)):
        result.append(deserialise(value[index], subtypes[index]))

    return tuple(result)


def deserialise_list(value: Any, subtype: Any) -> List[Any]:
    if value is None:
        return []
    result = []
    for item in value:
        result.append(deserialise(item, subtype[0]))
    return result


def deserialise_set(value: Any, subtype: Any) -> Set[Any]:
    if value is None:
        return set()
    result = []
    for item in value:
        result.append(deserialise(item, subtype[0]))
    return set(result)


def deserialise_frozenset(value, subtype) -> FrozenSet:
    if value is None:
        return frozenset()
    result = []
    for item in value:
        result.append(deserialise(item, subtype[0]))
    return frozenset(result)


COMPLEX_TYPE_DECODERS = {
    tuple: deserialise_tuple,
    list: deserialise_list,
    set: deserialise_set,
    frozenset: deserialise_frozenset,
    Literal: lambda value, subtypes: deserialise(value, type(value)),
}


def deserialise_dataclass(value: Any, source_type: Any) -> dict:
    result = source_type.__new__(source_type)
    for key, type_ in source_type.__annotations__.items():
        if key not in value:
            setattr(result, key, deserialise(None, type_))
            continue
        setattr(result, key, deserialise(value[key], type_))

    return result


def deserialise_typed_dict(value: Any, source_type: Any) -> Dict[Any, Any]:
    result = {}
    for key, type_ in source_type.__annotations__.items():
        if key not in value:
            result[key] = deserialise(None, type_)
            continue
        result[key] = deserialise(value[key], type_)

    return result


def deserialise(value: Any, source_type: Any) -> Any:

    # Lists, Sets, Tuples, Iterable
    origin_type = getattr(source_type, "__origin__", None)
    if origin_type and origin_type in COMPLEX_TYPE_DECODERS:
        if origin_type in COMPLEX_TYPE_DECODERS:
            return COMPLEX_TYPE_DECODERS[origin_type](value, source_type.__args__)

        return deserialise_list(value, source_type)

    # Nullables
    if value is None:
        return None

    # Gata types
    if issubclass(source_type, SerialisableType):
        return source_type.deserialise(value)

    # Dataclass
    if is_dataclass(source_type):
        return deserialise_dataclass(value, source_type)

    # Enums
    if issubclass(source_type, Enum):
        return source_type(value)

    # Pre-defined decoders
    if source_type in TYPE_DECODERS:
        return TYPE_DECODERS[source_type](value)  # type: ignore

    # Typed Dict
    if isclass(source_type) and is_typed_dict(source_type):
        return deserialise_typed_dict(value, source_type)

    # Unsupported
    raise DeserialisationError(f"Cannot deserialise value of type {source_type}")


__all__ = ["deserialise", "deserialise_dataclass"]
