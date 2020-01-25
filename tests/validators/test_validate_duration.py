from datetime import timedelta

import pytest

from gata.errors import ValidationError
from gata.validators import validate_duration


@pytest.mark.parametrize(
    "value", ("P1W", "PT1H", "P1W4DT1H1M20.5S"),
)
def test_valid_values(value: str) -> None:
    assert isinstance(validate_duration(value), timedelta)


@pytest.mark.parametrize("value", (None, "%%%", "@93004"))
def test_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        validate_duration(value)
