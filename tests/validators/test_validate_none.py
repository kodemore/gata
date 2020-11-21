import pytest

from gata.errors import ValidationError
from gata.validators import validate_none


@pytest.mark.parametrize("value", [None])
def test_valid_values(value: str):
    assert validate_none(value) is None


@pytest.mark.parametrize(
    "value",
    ("1", 1, True, False),
)
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_none(value)
