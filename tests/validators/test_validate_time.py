import pytest
from datetime import time
from gata.errors import ValidationError
from gata.validators import validate_time


@pytest.mark.parametrize(
    "value", ("17:34:02.124Z", "17:34:02.124Z", "17:34:02", "17:34:02.124")
)
def test_valid_values(value: str) -> None:
    assert isinstance(validate_time(value), time)


@pytest.mark.parametrize("value", ("25:34:02.124Z", "000", "17:3", "18:99:00"))
def test_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        validate_time(value)
