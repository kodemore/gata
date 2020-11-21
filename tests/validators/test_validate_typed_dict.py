import pytest

from gata.errors import ValidationError
from gata.validators import validate_date, validate_integer, validate_typed_dict


def test_valid_values() -> None:
    assert validate_typed_dict(
        {"name": 12, "dob": "2020-01-01"},
        {"name": validate_integer, "dob": validate_date},
    ) == {"name": 12, "dob": "2020-01-01",}


def test_invalid_values() -> None:
    with pytest.raises(ValidationError):
        validate_typed_dict(
            {"name": 12, "dob": "1"}, {"name": validate_integer, "dob": validate_date}
        )
