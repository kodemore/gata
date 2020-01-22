from datetime import date
import pytest

from gata.errors import ValidationError
from gata.validators import validate_date, validate_dict, validate_integer


def test_valid_values() -> None:
    assert validate_dict({"2019-10-20": 12}, validate_date, validate_integer) == {
        date(2019, 10, 20): 12
    }


def test_fail_on_invalid_key() -> None:
    with pytest.raises(ValidationError):
        validate_dict({"2019": 12}, validate_date, validate_integer)


def test_fail_on_invalid_value() -> None:
    with pytest.raises(ValidationError):
        validate_dict({"2019-10-20": "a"}, validate_date, validate_integer)
