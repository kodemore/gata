import re
from collections.abc import Iterable, Sequence
from dataclasses import MISSING, asdict, is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from functools import partial
from inspect import isclass
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Callable, Dict, Pattern, Type, Union
from uuid import UUID

from bson import ObjectId
from typing_extensions import Literal

from gata.errors import FieldError, FormatValidationError, TypeValidationError, ValidationError
from gata.format import Format
from gata.typing import ValidatableType
from gata.utils import DocString, is_optional_type, is_typed_dict, noop
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
    validate_object_id,
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
    if not pattern.match(value):
        raise FormatValidationError(expected_format=pattern)
    return value


def _build_list_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_list, item_validator=item_validator)


def _build_set_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_set, item_validator=item_validator)


def _build_tuple_validator(*args) -> Callable[..., Any]:
    item_validators = []
    for arg_type in args:
        item_validators.append(map_type_to_validator(arg_type))

    return partial(validate_tuple, item_validators=item_validators)


def _build_frozenset_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_frozenset, item_validator=item_validator)


def _build_iterable_validator(*args) -> Callable[..., Any]:
    item_validator = map_type_to_validator(args[0])
    return partial(validate_iterable, item_validator=item_validator)


def _build_dict_validator(*args) -> Callable[..., Any]:
    key_validator = map_type_to_validator(args[0])
    value_validator = map_type_to_validator(args[1])

    return partial(validate_dict, key_validator=key_validator, value_validator=value_validator)


def _build_union_validator(*args) -> Callable[..., Any]:

    # Optional type support
    if len(args) == 2 and isinstance(None, args[1]):
        return partial(validate_nullable, validator=map_type_to_validator(args[0]))

    validators = []
    for subtype in args:
        validators.append(map_type_to_validator(subtype))

    return partial(validate_any, validators=validators)


def _build_typed_dict_validator(**kwargs) -> Callable[..., Any]:

    validators = {}
    for key, key_type in kwargs.items():
        validators[key] = map_type_to_validator(key_type)

    return partial(validate_typed_dict, validator_map=validators)


def _build_pattern_validator(pattern: str) -> Callable[..., Any]:
    validate_pattern(pattern)
    compiled_pattern = re.compile(pattern)

    return partial(_validate_against_pattern, pattern=compiled_pattern)


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
    ObjectId: validate_object_id,
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
    Pattern: validate_pattern,
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
        return _COMPLEX_TYPE_VALIDATORS[origin_type](*subtype)  # type: ignore

    # Primitives
    if type_ in _TYPE_VALIDATORS:
        return _TYPE_VALIDATORS[type_]  # type: ignore

    # Typed dict
    if is_typed_dict(type_):
        return _build_typed_dict_validator(**type_.__annotations__)

    # Enums
    if isclass(type_) and issubclass(type_, Enum):
        return partial(validate_enum, enum_class=type_)

    return noop


def _build_min_max_validator(type_: Any, minimum: int, maximum: int) -> Callable[[Any], Any]:
    min_max_kwargs = {"minimum": minimum, "maximum": maximum}
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
    Format.BSON_OBJECT_ID: validate_object_id,
}


def map_str_format_to_validator(format_name: Union[str, Format]) -> Callable[[Any], Any]:
    if isinstance(format_name, str):
        format_name = Format(format_name)

    return _FORMAT_TO_VALIDATOR_MAP[format_name]


class _Undefined:
    pass


UNDEFINED = _Undefined()


class Field:
    def __init__(
        self,
        maximum: int = None,
        minimum: int = None,
        multiple_of: Union[int, float, Decimal] = None,
        string_format: Union[str, Format] = None,
        pattern: str = None,
        read_only: bool = None,
        write_only: bool = None,
        serialiser: Callable = None,
        deserialiser: Callable = None,
        default: Any = UNDEFINED,
        default_factory: Callable = UNDEFINED,
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.multiple_of = multiple_of
        self.string_format = string_format
        self.pattern = pattern
        self.read_only = read_only
        self.write_only = write_only
        self._type = None
        self._validator: Callable = None  # type: ignore
        self.serialiser = serialiser
        self.deserialiser = deserialiser
        self._default = default
        self._default_factory = default_factory

    @property
    def default(self) -> Any:
        if self._default_factory is not UNDEFINED:
            return self._default_factory()
        if self._default is not UNDEFINED:
            return self._default

        return UNDEFINED

    @property
    def type(self) -> Type[Any]:
        return self._type  # type: ignore

    @property
    def validator(self) -> Callable[[Any], Any]:
        if not self._validator:
            validators = [map_type_to_validator(self.type)]
            if self.minimum is not None or self.maximum is not None:
                validators.append(_build_min_max_validator(self._type, self.minimum, self.maximum))
            if self.pattern:
                validators.append(_build_pattern_validator(self.pattern))
            if self.multiple_of:
                validators.append(partial(validate_multiple_of, multiple_of=self.multiple_of))

            self._validator = partial(validate_all, validators=validators)

        return self._validator

    def validate(self, value) -> Any:
        self.validator(value)
        return value


class Reference(Field):
    def __init__(self, field_type, read_only: bool = None, write_only: bool = None):
        super().__init__(read_only=read_only, write_only=write_only)
        self._type = field_type
        self.reference = get_dataclass_schema(field_type)

    @property
    def validator(self) -> Callable[[Any], Any]:
        return self.reference.validate


class Schema:
    def __init__(self, dataclass_type: Any):
        if not is_dataclass(dataclass_type):
            raise ValueError("passed value is not valid dataclass type")
        self.doc_string = DocString(dataclass_type)
        self.type = dataclass_type
        self.class_name = dataclass_type.__name__
        self._fields: Dict[str, Field] = {}

    def __setitem__(self, key: str, value: Field):
        self._fields[key] = value

    def __getitem__(self, key: str) -> Field:
        return self._fields[key]

    def __contains__(self, key: str) -> bool:
        return key in self._fields

    def __iter__(self) -> Iterable:
        return iter(self._fields.items())

    def validate(self, value: Dict[str, Any]) -> Any:
        if isinstance(value, self.type):  # self validating fix
            return value

        for key, field in self._fields.items():
            try:
                field_value = value.get(key, None)
                if field_value is None:
                    if is_optional_type(field.type) or field.read_only:
                        continue
                    raise FieldError(key, TypeValidationError(expected_type=field.type))

                field.validate(field_value)
            except ValidationError as error:
                raise FieldError(key, error)

        return value


_SCHEMAS: Dict[Any, Schema] = {}


def get_dataclass_schema(dataclass_class: Any) -> Schema:
    if dataclass_class in _SCHEMAS:
        return _SCHEMAS[dataclass_class]

    schema = Schema(dataclass_class)
    _SCHEMAS[dataclass_class] = schema

    schema_fields = object()
    if hasattr(dataclass_class, "Schema"):
        schema_fields = dataclass_class.Schema

    for field_name, field in dataclass_class.__dataclass_fields__.items():
        schema[field_name] = getattr(schema_fields, field_name) if hasattr(schema_fields, field_name) else Field()
        schema[field_name]._type = field.type
        if field.default is not MISSING:
            schema[field_name]._default = field.default
        if field.default_factory is not MISSING:
            schema[field_name]._default_factory = field.default_factory

        # reference type
        if is_dataclass(field.type):
            schema[field_name] = Reference(field.type, schema[field_name].read_only, schema[field_name].write_only)

        custom_serialiser = f"serialise_{field_name}"
        if hasattr(schema_fields, custom_serialiser):
            schema[field_name].serialiser = getattr(schema_fields, custom_serialiser)

        custom_deserialiser = f"deserialise_{field_name}"
        if hasattr(schema_fields, custom_deserialiser):
            schema[field_name].deserialiser = getattr(schema_fields, custom_deserialiser)

    return schema


def validate(value, dataclass_class: Any = None) -> Any:
    if dataclass_class is None:
        if not hasattr(value, "__class__"):
            raise ValueError(f"could not validate value {value}, please provide dataclass_class parameter")
        dataclass_class = value.__class__

    schema = get_dataclass_schema(dataclass_class)
    if not isinstance(value, dict):
        value = asdict(value)

    return schema.validate(value)


__all__ = [
    "Field",
    "Format",
    "Reference",
    "Schema",
    "validate",
    "get_dataclass_schema",
    "map_type_to_validator",
    "UNDEFINED",
]
