from datetime import date

import pytest

from gata.errors import ValidationError
from gata.validators import validate_date


@pytest.mark.parametrize("value", ["2016-09-18", "20160918"])
def test_valid_values(value: str) -> None:
    assert isinstance(validate_date(value), date)


@pytest.mark.parametrize("value", ["2016-13-18", "20161318", "1209"])
def test_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        validate_date(value)
