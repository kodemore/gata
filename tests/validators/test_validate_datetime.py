from datetime import datetime

import pytest

from gata.errors import ValidationError
from gata.validators import validate_datetime


@pytest.mark.parametrize(
    "value",
    (
        "2016-09-18T17:34:02.124Z",
        "2016-09-18 17:34:02.124Z",
        "2016-09-1817:34:02.124Z",
        "2016-09-1817:34:02Z",
        "2016-09-18T17:34:02+02:00",
        "20160918173402Z",
    ),
)
def test_valid_values(value: str) -> None:
    assert isinstance(validate_datetime(value), datetime)


@pytest.mark.parametrize("value", ["2016-13-18", "20161318", "1209", "2016-13-30T17:34:02.124Z"])
def test_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        validate_datetime(value)
