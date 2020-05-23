from typing import Callable

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

__all__ = ["Validator"]


def _make_assert(validator: Callable) -> Callable:
    def _validate(*args, **kwargs) -> bool:
        try:
            validator(*args, **kwargs)
            return True
        except ValueError:
            return False

    return _validate


class Validator:
    assert_all = _make_assert(validate_all)
    assert_any = _make_assert(validate_any)
    assert_array = _make_assert(validate_iterable)
    assert_boolean = _make_assert(validate_boolean)
    assert_bytes = _make_assert(validate_bytes)
    assert_datetime = _make_assert(validate_datetime)
    assert_date = _make_assert(validate_date)
    assert_decimal = _make_assert(validate_decimal)
    assert_duration = _make_assert(validate_duration)
    assert_email = _make_assert(validate_email)
    assert_enum = _make_assert(validate_enum)
    assert_float = _make_assert(validate_float)
    assert_frozenset = _make_assert(validate_frozenset)
    assert_hostname = _make_assert(validate_hostname)
    assert_integer = _make_assert(validate_integer)
    assert_ipv4 = _make_assert(validate_ipv4)
    assert_ipv6 = _make_assert(validate_ipv6)
    assert_items = _make_assert(validate_iterable_items)
    assert_length = _make_assert(validate_length)
    assert_list = _make_assert(validate_list)
    assert_literal = _make_assert(validate_literal)
    assert_multiple_of = _make_assert(validate_multiple_of)
    assert_nullable = _make_assert(validate_nullable)
    assert_object_id = _make_assert(validate_object_id)
    assert_pattern = _make_assert(validate_pattern)
    assert_range = _make_assert(validate_range)
    assert_semver = _make_assert(validate_semver)
    assert_set = _make_assert(validate_set)
    assert_string = _make_assert(validate_string)
    assert_time = _make_assert(validate_time)
    assert_tuple = _make_assert(validate_tuple)
    assert_uri = _make_assert(validate_uri)
    assert_url = _make_assert(validate_url)
    assert_uuid = _make_assert(validate_uuid)
