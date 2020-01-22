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
    for index in range(len(subtypes)):
        result.append(serialise(value[index], subtypes[index]))

    return result


def serialise_iterable(value: Iterable[Any], subtypes: List[Any]) -> List[Any]:
    if not subtypes:
        raise SerialisationError(
            "Cannot serialise generic iterables please assure subtype is defined between [ and ]"
        )

    result = []
    for item in value:
        result.append(serialise(item, subtypes[0]))

    return result


COMPLEX_TYPE_ENCODERS = {
    tuple: serialise_tuple,
    list: serialise_iterable,
    set: serialise_iterable,
    frozenset: serialise_iterable,
    Literal: lambda value, subtypes: serialise(value, type(value)),
}


def serialise_dataclass(value: Any, source_type: Any) -> dict:
    result = {}
    for key, type_ in source_type.__annotations__.items():
        result[key] = serialise(getattr(value, key), type_)

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
        if value is None:
            return []

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
