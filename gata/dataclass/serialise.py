from base64 import b64encode
from dataclasses import is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from inspect import isclass
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Callable, Dict, Iterable, List, Tuple, Union
from uuid import UUID

from bson import ObjectId
from typing_extensions import Literal

from gata.errors import SerialisationError
from gata.typing import SerialisableType
from gata.utils import is_typed_dict
from .schema import get_dataclass_schema

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
    Any: lambda value: value,
    ObjectId: str,
}


def serialise_tuple(
    value: Tuple[Any, ...], subtypes: List[Any], mapping: Dict[str, Union[bool, str, dict, Callable]] = None,
) -> List[Any]:
    if not subtypes:
        raise SerialisationError("Cannot serialise generic tuples, please assure subtype is defined.")
    result = []
    if value is None:
        return result

    if ... in subtypes:
        item_type = subtypes[0]
        for index in range(len(value)):
            result.append(serialise(value[index], item_type, mapping))
    else:
        for index in range(len(subtypes)):
            result.append(serialise(value[index], subtypes[index], mapping))

    return result


def serialise_iterable(
    value: Iterable[Any], subtypes: List[Any], mapping: Dict[str, Union[bool, str, dict, Callable]] = None,
) -> List[Any]:
    if not subtypes:
        raise SerialisationError("Cannot serialise generic iterables please assure subtype is defined between [ and ]")

    result = []
    if value is None:
        return result

    for item in value:
        result.append(serialise(item, subtypes[0], mapping))

    if mapping and "$item" in mapping:
        return [item[mapping["$item"]] for item in result if mapping["$item"] in item]

    return result


def serialise_union(value, subtypes: List[Any], mapping: Dict[str, Union[bool, str, dict, Callable]] = None,) -> Any:
    # Optional values
    if value is None and NoneType in subtypes:  # type: ignore
        return None

    value_type = type(value)

    # Known listed type
    if value_type in subtypes:
        return serialise(value, value_type, mapping)

    for subtype in subtypes:
        if issubclass(subtype, value_type):
            return subtype.serialise(value)

    raise SerialisationError(f"Cannot serialise value of type {value_type}")


COMPLEX_TYPE_ENCODERS = {
    tuple: serialise_tuple,
    list: serialise_iterable,
    set: serialise_iterable,
    frozenset: serialise_iterable,
    Literal: lambda value, subtypes, mapping: serialise(value, type(value)),
    Union: serialise_union,
}


def _add_key_to_result(
    result: Dict[str, Any], key: str, value: Any, field_type: Any, mapping: Dict[str, Union[bool, str, dict, Callable]],
) -> None:
    if mapping is None or key not in mapping:
        result[key] = serialise(value, field_type)
        return None

    item_key = mapping[key]

    if isinstance(item_key, str):
        result[item_key] = serialise(value, field_type)
        return None

    if isinstance(item_key, bool):
        if not item_key:
            return None
        result[key] = serialise(value, field_type)
        return None

    if isinstance(item_key, dict):
        if "$self" in item_key:
            result[item_key["$self"]] = serialise(value, field_type, item_key)
        else:
            result[key] = serialise(value, field_type, item_key)
        return None

    if callable(item_key):
        user_serialised = item_key(value)  # type: Tuple[str, Any]
        if not isinstance(user_serialised[0], str):
            raise ValueError(
                f"user mapping returned invalid value for key {key},callable should return field name and field value,"
                + "please refer to mapping section in gata's documentation"
            )

        result[user_serialised[0]] = user_serialised[1]
        return None

    raise ValueError(f"unsupported mapping option for key {key}, mapping supports boo, str, dict, callable values only")


def serialise_dataclass(
    value: Any, source_type: Any, mapping: Dict[str, Union[bool, str, dict, Callable]] = None,
) -> Dict[str, Any]:
    result = {}  # type: Dict[str, Any]
    class_schema = get_dataclass_schema(value.__class__)
    for key, field in source_type.__dataclass_fields__.items():
        schema_field = class_schema[key]
        if schema_field.write_only:
            continue

        if schema_field.serialiser:
            result_value = schema_field.serialiser(getattr(value, key))
            # support very basic mapping
            if mapping and key in mapping and isinstance(mapping[key], str):
                result[mapping[key]] = result_value  # type: ignore
            else:
                result[key] = result_value
            continue

        if mapping:
            _add_key_to_result(result, key, getattr(value, key), field.type, mapping)
            continue

        result[key] = serialise(getattr(value, key), field.type)

    return result


def serialise_typed_dict(
    value: Any, source_type: Any, mapping: Dict[str, Union[bool, str, dict, Callable]] = None,
) -> Dict[str, Any]:
    result = {}  # type: Dict[str, Any]
    for key, type_ in source_type.__annotations__.items():
        if mapping:
            _add_key_to_result(result, key, value[key], type_, mapping)
            continue

        result[key] = serialise(value[key], type_)

    return result


def serialise(value: Any, source_type: Any, mapping: Dict[str, Union[bool, str, dict, Callable]] = None,) -> Any:

    # Lists, Sets, Tuples, Iterable
    origin_type = getattr(source_type, "__origin__", None)
    if origin_type and origin_type in COMPLEX_TYPE_ENCODERS:
        if origin_type in COMPLEX_TYPE_ENCODERS:
            return COMPLEX_TYPE_ENCODERS[origin_type](  # type: ignore
                value, source_type.__args__, mapping
            )

        return serialise_iterable(value, source_type)

    # Nullables
    if value is None:
        return None

    # Dataclass
    if is_dataclass(source_type):
        return serialise_dataclass(value, source_type, mapping)

    # Typed Dict
    if isclass(source_type) and is_typed_dict(source_type):
        return serialise_typed_dict(value, source_type, mapping)

    # Gata types
    if isclass(source_type) and issubclass(source_type, SerialisableType):
        return source_type.serialise(value)

    # Enums
    if isinstance(value, Enum):
        return value.value

    # Pre-defined encoders
    if source_type in TYPE_ENCODERS:
        return TYPE_ENCODERS[source_type](value)  # type: ignore

    # Unsupported
    raise SerialisationError(f"Cannot serialise value of type {source_type}")


__all__ = ["serialise", "serialise_dataclass"]
