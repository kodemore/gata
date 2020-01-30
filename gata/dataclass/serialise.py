from base64 import b64encode
from dataclasses import is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from inspect import isclass
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Iterable, List, Tuple, Union
from uuid import UUID

from typing_extensions import Literal

from gata.errors import SerialisationError
from gata.typing import SerialisableType
from gata.utils import is_typed_dict


NoneType = type(None)


def serialise_datetype(value: Union[date, datetime, time]) -> str:
    return value.isoformat()


TYPE_ENCODERS = {
    IPv4Address: str,
    IPv6Address: str,
    UUID: str,
    datetime: serialise_datetype,
    date: serialise_datetype,
    time: serialise_datetype,
    bool: bool,
    int: int,
    float: float,
    str: str,
    bytes: lambda value: b64encode(value).decode("utf8"),
    Decimal: str,
}


def serialise_tuple(value: Tuple[Any, ...], subtypes: List[Any]) -> List[Any]:
    if not subtypes:
        raise SerialisationError(
            "Cannot serialise generic tuples, please assure subtype is defined."
        )
    result = []
    if value is None:
        return result

    if ... in subtypes:
        item_type = subtypes[0]
        for index in range(len(value)):
            result.append(serialise(value[index], item_type))
    else:
        for index in range(len(subtypes)):
            result.append(serialise(value[index], subtypes[index]))

    return result


def serialise_iterable(value: Iterable[Any], subtypes: List[Any]) -> List[Any]:
    if not subtypes:
        raise SerialisationError(
            "Cannot serialise generic iterables please assure subtype is defined between [ and ]"
        )

    result = []
    if value is None:
        return result

    for item in value:
        result.append(serialise(item, subtypes[0]))

    return result


def serialise_union(value, subtypes: List[Any]) -> Any:
    # Optional values
    if value is None and NoneType in subtypes:  # type: ignore
        return None

    value_type = type(value)

    # Known listed type
    if value_type in subtypes:
        return serialise(value, value_type)

    for subtype in subtypes:
        if issubclass(subtype, value_type):
            return subtype.serialise(value)

    raise SerialisationError(f"Cannot serialise value of type {value_type}")


COMPLEX_TYPE_ENCODERS = {
    tuple: serialise_tuple,
    list: serialise_iterable,
    set: serialise_iterable,
    frozenset: serialise_iterable,
    Literal: lambda value, subtypes: serialise(value, type(value)),
    Union: serialise_union,
}


def serialise_dataclass(value: Any, source_type: Any) -> dict:
    result = {}
    properties_meta = (
        getattr(source_type, "Meta") if hasattr(source_type, "Meta") else {}
    )
    for key, field in source_type.__dataclass_fields__.items():
        write_only = False
        if hasattr(properties_meta, key):
            property_meta = getattr(properties_meta, key)
            if "write_only" in property_meta and property_meta["write_only"]:
                write_only = True

        if write_only:
            continue

        result[key] = serialise(getattr(value, key), field.type)

    return result


def serialise_typed_dict(value: Any, source_type: Any) -> dict:
    result = {}
    for key, type_ in source_type.__annotations__.items():
        result[key] = serialise(value[key], type_)

    return result


def serialise(value: Any, source_type: Any) -> Any:

    # Lists, Sets, Tuples, Iterable
    origin_type = getattr(source_type, "__origin__", None)
    if origin_type and origin_type in COMPLEX_TYPE_ENCODERS:
        if origin_type in COMPLEX_TYPE_ENCODERS:
            return COMPLEX_TYPE_ENCODERS[origin_type](value, source_type.__args__)

        return serialise_iterable(value, source_type)

    # Nullables
    if value is None:
        return None

    # Gata types
    if isclass(source_type) and issubclass(source_type, SerialisableType):
        return source_type.serialise(value)

    # Dataclass
    if is_dataclass(source_type):
        return serialise_dataclass(value, source_type)

    # Enums
    if isinstance(value, Enum):
        return value.value

    # Pre-defined encoders
    if source_type in TYPE_ENCODERS:
        return TYPE_ENCODERS[source_type](value)  # type: ignore

    # Typed Dict
    if isclass(source_type) and is_typed_dict(source_type):
        return serialise_typed_dict(value, source_type)

    # Unsupported
    raise SerialisationError(f"Cannot serialise value of type {source_type}")


__all__ = ["serialise", "serialise_dataclass"]
