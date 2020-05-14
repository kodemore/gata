import dataclasses
import datetime
import decimal
import ipaddress
import re
from typing import Any, AnyStr, ByteString, Dict, List as GenericList
import uuid

import bson

from gata.inspect import is_dataclass_like
from gata.schema import Field, Schema
from gata.typing import *

SUPPORTED_TYPES = {
    bool: Boolean,
    int: Integer,
    float: Float,
    str: String,
    bytes: Bytes,
    bytearray: Bytes,
    list: List,
    GenericList: List,
    decimal.Decimal: Decimal,
    datetime.date: Date,
    datetime.datetime: DateTime,
    datetime.time: Time,
    datetime.timedelta: Duration,
    re.Pattern: RegexPattern,
    ipaddress.IPv4Address: Ipv4Address,
    ipaddress.IPv6Address: Ipv6Address,
    uuid.UUID: UUID,
    bson.ObjectId: ObjectId,
    Any: AnyType,
    ByteString: Bytes,
    AnyStr: String,
}


def _ignore(value: Any) -> Any:
    return value


def map_python_type_to_schema_type(python_type: Any, type_properties: Dict[str, Any]) -> Any:

    if python_type in SUPPORTED_TYPES:
        return SUPPORTED_TYPES[python_type](**type_properties)

    origin_type = getattr(python_type, "__origin__", None)
    if origin_type is None:
        if python_type in SUPPORTED_TYPES:
            return SUPPORTED_TYPES[python_type](**type_properties)
        return None
    if origin_type not in SUPPORTED_TYPES:
        return AnyType()

    subtypes = []
    for python_subtype in python_type.__args__:
        subtypes.append(
            map_python_type_to_schema_type(
                python_subtype,
                type_properties["items"] if "items" in type_properties else {}
            )
        )

    init_args = {**type_properties, **{"items": subtypes}}

    return SUPPORTED_TYPES[origin_type](**init_args)


def build_schema(_cls: Any) -> Schema:
    if not is_dataclass_like(_cls):
        raise ValueError(f"passed value {_cls} is not valid dataclass type")

    schema = Schema(_cls)
    for field_name, field_type in _cls.__annotations__.items():
        field_descriptor = Field()

        if hasattr(_cls, field_name):
            field_value = getattr(_cls, field_name)
            if isinstance(field_value, dataclasses.Field):
                field_descriptor.compare = field_value.compare
                field_descriptor.repr = field_value.repr
                field_descriptor._default = field_value.default
                field_descriptor._default_factory = field_value.default_factory  # type: ignore
            elif isinstance(field_value, Field):
                field_descriptor = field_value
            else:
                field_descriptor._default = field_value

        field_descriptor._original_type = field_type

        field_properties = {
            "minimum": field_descriptor.minimum,
            "maximum": field_descriptor.maximum,
            "multiple_of": field_descriptor.multiple_of,
            "format": field_descriptor.format,
            "items": field_descriptor.items,
            "pattern": field_descriptor.pattern,
        }

        field_descriptor._type = map_python_type_to_schema_type(field_type, field_properties)

        schema[field_name] = field_descriptor

    return schema
