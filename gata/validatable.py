from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Dict, TypeVar, Union

from typing_extensions import Protocol

from .dataclass.schema import get_dataclass_schema
from .utils import convert_to_dataclass
from .validators import (
    validate_all,
    validate_any,
    validate_boolean,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_decimal,
    validate_duration,
    validate_email,
    validate_enum,
    validate_float,
    validate_frozenset,
    validate_hostname,
    validate_integer,
    validate_ipv4,
    validate_ipv6,
    validate_iterable,
    validate_iterable_items,
    validate_length,
    validate_list,
    validate_literal,
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
    validate_uri,
    validate_url,
    validate_uuid,
)

T = TypeVar("T")


class Validatable(Protocol):
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        ...


def validatable(_cls: T = None,) -> Union[T, Validatable, Callable[[Any], Union[T, Validatable]]]:
    def _attach_validatable_interface(_cls) -> Union[T, Validatable]:
        if not is_dataclass(_cls):
            _cls = convert_to_dataclass(_cls)

        schema = get_dataclass_schema(_cls)
        old_init = getattr(_cls, "__init__")

        def _init(*args, **kwargs):
            self = args[0]
            old_init(*args, **kwargs)
            schema.validate(asdict(self))

        setattr(_cls, "__init__", _init)
        setattr(_cls, "validate", lambda value: schema.validate(value))

        return _cls

    if _cls is None:
        return _attach_validatable_interface

    return _attach_validatable_interface(_cls)


class Validator:
    all = validate_all
    any = validate_any
    array = validate_iterable
    boolean = validate_boolean
    bytes = validate_bytes
    datetime = validate_datetime
    date = validate_date
    decimal = validate_decimal
    duration = validate_duration
    email = validate_email
    enum = validate_enum
    float = validate_float
    frozenset = validate_frozenset
    hostname = validate_hostname
    integer = validate_integer
    ipv4 = validate_ipv4
    ipv6 = validate_ipv6
    items = validate_iterable_items
    length = validate_length
    list = validate_list
    literal = validate_literal
    multiple_of = validate_multiple_of
    nullable = validate_nullable
    object_id = validate_object_id
    pattern = validate_pattern
    range = validate_range
    semver = validate_semver
    set = validate_set
    string = validate_string
    time = validate_time
    tuple = validate_tuple
    uri = validate_uri
    url = validate_url
    uuid = validate_uuid


__all__ = ["validatable", "Validatable", "Validator"]
