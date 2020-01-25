from collections.abc import Iterable, Sequence
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from functools import partial
from inspect import isclass
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Callable, Dict, Pattern, Union
from uuid import UUID
import re

from typing_extensions import Literal

from gata.errors import (
    FieldError,
    ValidationError,
    FormatValidationError,
    TypeValidationError,
)
from gata.format import Format
from gata.typing import ValidatableType
from gata.utils import DocString, is_typed_dict, noop, is_optional_type
from gata.validators import (
    validate_all,
    validate_any,
    validate_boolean,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_decimal,
    validate_dict,
    validate_email,
    validate_enum,
    validate_float,
    validate_frozenset,
    validate_hostname,
    validate_integer,
    validate_ipv4,
    validate_ipv6,
    validate_iterable,
    validate_length,
    validate_list,
    validate_multiple_of,
    validate_nullable,
    validate_pattern,
    validate_range,
    validate_semver,
    validate_set,
    validate_string,
    validate_time,
    validate_tuple,
    validate_typed_dict,
    validate_uri,
    validate_url,
    validate_uuid,
)


def _validate_against_pattern(value: Any, pattern: Pattern[str]) -> str:
    value = validate_string(value)
    if pattern.match(value):
        return value
    raise FormatValidationError(expected_format=pattern)


def _build_list_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_list, item_validator=item_validator,)


def _build_set_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_set, item_validator=item_validator,)


def _build_tuple_validator(*args) -> Callable[..., Any]:
    item_validators = []
    for arg_type in args:
        item_validators.append(map_type_to_validator(arg_type))

    return partial(validate_tuple, item_validators=item_validators,)


def _build_frozenset_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_frozenset, item_validator=item_validator,)


def _build_iterable_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_iterable, item_validator=item_validator,)


def _build_dict_validator(*args) -> Callable[..., Any]:
    key_validator = map_type_to_validator(args[0])
    value_validator = map_type_to_validator(args[1])

    return partial(
        validate_dict, key_validator=key_validator, value_validator=value_validator
    )


def _build_union_validator(*args) -> Callable[..., Any]:

    # Optional type support
    if len(args) == 2 and isinstance(None, args[1]):
        return partial(validate_nullable, validator=map_type_to_validator(args[0]))

    validators = []
    for subtype in args:
        validators.append(map_type_to_validator(subtype))

    return partial(validate_any, validators=validators)


def build_typed_dict_validator(**kwargs) -> Callable[..., Any]:

    validators = {}
    for key, key_type in kwargs.items():
        validators[key] = map_type_to_validator(key_type)

    return partial(validate_typed_dict, validator_map=validators)


def _build_pattern_validator(*args) -> Callable[..., Any]:
    return validate_pattern


def _build_literal_validator(*args) -> Callable[..., Any]:
    def _validate_literal(value: Any) -> Any:
        if value in args:
            return value
        raise ValidationError("Passed value is not listed in Literal.")

    return _validate_literal


_TYPE_VALIDATORS = {
    Any: lambda x: None,
    bool: validate_boolean,
    int: validate_integer,
    float: validate_float,
    str: validate_string,
    list: validate_list,
    set: validate_set,
    frozenset: validate_frozenset,
    bytes: validate_bytes,
    date: validate_date,
    datetime: validate_datetime,
    time: validate_time,
    Iterable: validate_iterable,
    IPv4Address: validate_ipv4,
    IPv6Address: validate_ipv6,
    Pattern: validate_pattern,
    Decimal: validate_decimal,
    UUID: validate_uuid,
}

_COMPLEX_TYPE_VALIDATORS = {
    list: _build_list_validator,
    tuple: _build_tuple_validator,
    set: _build_set_validator,
    frozenset: _build_frozenset_validator,
    Iterable: _build_iterable_validator,
    Sequence: _build_iterable_validator,
    dict: _build_dict_validator,
    Union: _build_union_validator,
    Pattern: _build_pattern_validator,
    Literal: _build_literal_validator,
}


def map_type_to_validator(type_: Any) -> Callable[[Any], Any]:
    # Gata types
    if isclass(type_) and issubclass(type_, ValidatableType):
        return type_.validate

    # Lists, Sets, Tuples, Iterable
    origin_type = getattr(type_, "__origin__", None)
    if origin_type and origin_type in _COMPLEX_TYPE_VALIDATORS:
        subtype = type_.__args__
        return _COMPLEX_TYPE_VALIDATORS[origin_type](*subtype)

    # Primitives
    if type_ in _TYPE_VALIDATORS:
        return _TYPE_VALIDATORS[type_]  # type: ignore

    if is_typed_dict(type_):
        return build_typed_dict_validator(**type_.__annotations__)

    # Enums
    if isclass(type_) and issubclass(type_, Enum):
        return partial(validate_enum, enum_class=type_)

    return noop


def build_min_max_validator(type_: Any, meta: Dict[str, int]) -> Callable[[Any], Any]:
    min_max_kwargs = {
        "minimum": meta.get("min"),
        "maximum": meta.get("max"),
    }
    if type_ in (int, float, Decimal):
        return partial(validate_range, **min_max_kwargs)
    else:
        return partial(validate_length, **min_max_kwargs)


_FORMAT_TO_VALIDATOR_MAP = {
    Format.DATETIME: validate_datetime,
    Format.DATE: validate_date,
    Format.TIME: validate_time,
    Format.URI: validate_uri,
    Format.URL: validate_url,
    Format.EMAIL: validate_email,
    Format.UUID: validate_uuid,
    Format.HOSTNAME: validate_hostname,
    Format.IPV4: validate_ipv4,
    Format.IPV6: validate_ipv6,
    Format.BOOLEAN: validate_boolean,
    Format.SEMVER: validate_semver,
    Format.BYTE: validate_bytes,
}


def map_str_format_to_validator(
    format_name: Union[str, Format]
) -> Callable[[Any], Any]:
    if isinstance(format_name, str):
        format_name = Format(format_name)

    return _FORMAT_TO_VALIDATOR_MAP[format_name]


def map_meta_to_validator(type_: Any, meta: Dict[str, Any]) -> Callable[[Any], Any]:
    meta_validators = []
    if "min" in meta or "max" in meta:
        meta_validators.append(build_min_max_validator(type_, meta))

    if type_ is str and "format" in meta:
        meta_validators.append(map_str_format_to_validator(meta["format"]))

    if "multiple_of" in meta:
        meta_validators.append(
            partial(validate_multiple_of, multiple_of=meta["multiple_of"])
        )

    if "pattern" in meta:
        pattern = re.compile(meta["pattern"], re.I)
        meta_validators.append(partial(_validate_against_pattern, pattern=pattern))

    def _validator(value: Any) -> Any:
        # None values should not be validated against meta
        if value is None:
            return None
        return partial(validate_all, validators=meta_validators)(value)

    return _validator


class FieldSchema:
    def __init__(self, field_type, field_meta: dict):
        self.type = field_type
        self.meta = field_meta
        self._validator: Callable = None  # type: ignore

    @property
    def validator(self) -> Callable[[Any], Any]:
        if not self._validator:
            self._validator = map_type_to_validator(self.type)
        return self._validator

    def validate(self, value) -> Any:
        self.validator(value)
        return value


class Reference(FieldSchema):
    def __init__(self, field_type, field_meta: dict):
        self.reference = get_dataclass_schema(field_type)
        super().__init__(field_type, field_meta)

    @property
    def validator(self) -> Callable[[Any], Any]:
        return self.reference.validate


class ClassSchema:
    def __init__(self, dataclass_type: Any):
        if not isclass(dataclass_type) or not is_dataclass(dataclass_type):
            raise ValueError("Passed value is not valid dataclass type.")
        self.doc_string = DocString(dataclass_type)
        self.type = dataclass_type
        self.class_name = dataclass_type.__name__
        self._attributes: Dict[str, FieldSchema] = {}

    def __setitem__(self, key: str, value: FieldSchema):
        self._attributes[key] = value

    def __getitem__(self, key: str) -> FieldSchema:
        return self._attributes[key]

    def __contains__(self, key: str) -> bool:
        return key in self._attributes

    def validate(self, value: Dict[str, Any]):
        for key, field in self._attributes.items():
            try:
                field_value = value.get(key, None)
                if field_value is None and isinstance(field, Reference):
                    if is_optional_type(field.type):
                        continue
                    raise FieldError(key, TypeValidationError(expected_type=field.type))

                field.validate(field_value)
            except ValidationError as error:
                raise FieldError(key, error)

        return value


_SCHEMAS: Dict[Any, ClassSchema] = {}


def get_dataclass_schema(dataclass_class: Any) -> ClassSchema:
    if dataclass_class in _SCHEMAS:
        return _SCHEMAS[dataclass_class]

    schema = ClassSchema(dataclass_class)
    _SCHEMAS[dataclass_class] = schema

    meta = dataclass_class.Meta if hasattr(dataclass_class, "Meta") else None
    for field, type_ in dataclass_class.__annotations__.items():
        if is_dataclass(type_):
            schema[field] = Reference(type_, {})
        else:
            field_meta = getattr(meta, field, {}) if meta else {}
            schema[field] = FieldSchema(type_, field_meta)

    return schema


def validate(value, dataclass_class: Any = None) -> Any:
    schema = get_dataclass_schema(dataclass_class)
    if not isinstance(value, dict):
        value = asdict(value)

    return schema.validate(value)


__all__ = [
    "FieldSchema",
    "Reference",
    "ClassSchema",
    "validate",
    "get_dataclass_schema",
    "map_type_to_validator",
    "map_meta_to_validator",
]
