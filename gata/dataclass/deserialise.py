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

from gata.errors import DeserialisationError, MetaError
from gata.typing import SerialisableType
from gata.utils import (
    is_typed_dict,
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_time_string,
)


NoneType = type(None)


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
    if ... in subtypes:
        item_type = subtypes[0]
        for index in range(len(value)):
            result.append(deserialise(value[index], item_type))
    else:
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


def deserialise_union(value, subtypes: List[Any]) -> Any:
    # Optional values
    if value is None and NoneType in subtypes:  # type: ignore
        return None

    value_type = type(value)

    # Known listed type
    if value_type in subtypes:
        return value

    # dataclass or typed dict
    dataclasses = [
        dataclass_type for dataclass_type in subtypes if is_dataclass(dataclass_type)
    ]
    if value_type is dict and dataclasses:

        keys = value.keys()
        for possible_type in dataclasses:
            if keys == possible_type.__dataclass_fields__.keys():
                return deserialise(value, possible_type)

    # try to deserialise by subtype
    for try_type in subtypes:
        try:
            return deserialise(value, try_type)
        except Exception:
            continue

    raise DeserialisationError(f"Cannot deserialise value to type {value_type}")


COMPLEX_TYPE_DECODERS = {
    tuple: deserialise_tuple,
    list: deserialise_list,
    set: deserialise_set,
    frozenset: deserialise_frozenset,
    Literal: lambda value, subtypes: deserialise(value, type(value)),
    Union: deserialise_union,
}


def deserialise_dataclass(value: Any, source_type: Any) -> dict:
    result = source_type.__new__(source_type)
    properties_meta = (
        getattr(source_type, "Meta") if hasattr(source_type, "Meta") else {}
    )
    for key, field in source_type.__dataclass_fields__.items():
        read_only = False
        if hasattr(properties_meta, key):
            property_meta = getattr(properties_meta, key)
            if "read_only" in property_meta and property_meta["read_only"]:
                read_only = True

        if read_only:
            continue

        custom_deserialiser_name = f"deserialise_{key}"
        if hasattr(properties_meta, custom_deserialiser_name):
            custom_deserialiser = getattr(properties_meta, custom_deserialiser_name)
            if not callable(custom_deserialiser):
                raise MetaError(
                    f"could not use deserialiser {custom_deserialiser_name} in {source_type}, deserialiser must be static method"
                )
            setattr(
                result, key, custom_deserialiser(value[key] if key in value else None)
            )
            continue

        if key not in value:
            setattr(result, key, deserialise(None, field.type))
            continue

        setattr(result, key, deserialise(value[key], field.type))

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
