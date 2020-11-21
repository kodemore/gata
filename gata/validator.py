from typing import Any
from typing import Callable

from gata import bson_support
from .validators import validate_all
from .validators import validate_any
from .validators import validate_boolean
from .validators import validate_bytes
from .validators import validate_date
from .validators import validate_datetime
from .validators import validate_decimal
from .validators import validate_duration
from .validators import validate_email
from .validators import validate_enum
from .validators import validate_float
from .validators import validate_frozenset
from .validators import validate_hostname
from .validators import validate_integer
from .validators import validate_ipv4
from .validators import validate_ipv6
from .validators import validate_iterable
from .validators import validate_iterable_items
from .validators import validate_length
from .validators import validate_list
from .validators import validate_literal
from .validators import validate_multiple_of
from .validators import validate_nullable
from .validators import validate_pattern
from .validators import validate_range
from .validators import validate_semver
from .validators import validate_set
from .validators import validate_string
from .validators import validate_time
from .validators import validate_tuple
from .validators import validate_uri
from .validators import validate_url
from .validators import validate_uuid

__all__ = ["Validator"]


def _make_assert(validator: Callable) -> Callable:
    def _validate(*args, **kwargs) -> bool:
        try:
            validator(*args, **kwargs)
            return True
        except ValueError:
            return False

    return _validate


def bson_not_supported(*args: Any) -> None:
    raise RuntimeError("Bson is not installed")


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
    assert_object_id = bson_not_supported


if bson_support.BSON_SUPPORT:
    Validator.assert_object_id = _make_assert(bson_support.validate_object_id)
