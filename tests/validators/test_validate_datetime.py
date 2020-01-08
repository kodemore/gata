import pytest

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
def test_valid_values(value: str):
    assert validate_datetime(value)
