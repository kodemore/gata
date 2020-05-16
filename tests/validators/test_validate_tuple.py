import pytest

from gata.errors import ValidationError
from gata.validators import validate_tuple, validate_integer, validate_string, validate_float


def test_validate_tuple() -> None:
    assert validate_tuple(tuple([1, 2, 3]))


def test_validate_tuple_with_partial_subtypes() -> None:
    assert validate_tuple(tuple([1, 2, 3]), [validate_integer, ...])


def test_validate_tuple_with_full_subtypes() -> None:
    assert validate_tuple(tuple([1, "a", 3.0]), [validate_integer, validate_string, validate_float])


def test_fail_with_ellipsis_only_subtype() -> None:
    with pytest.raises(TypeError):
        validate_tuple(tuple([1, 2, 3]), [...])


def test_validate_tuple_with_invalid_values() -> None:
    with pytest.raises(ValidationError):
        validate_tuple(tuple([1, 2, 'a']), [validate_integer, ...])

