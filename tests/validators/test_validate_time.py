import pytest

from gata.validators import validate_time


@pytest.mark.parametrize(
    "value", ("17:34:02.124Z", "17:34:02.124Z", "17:34:02", "17:34:02.124")
)
def test_valid_values(value: str):
    assert validate_time(value) is None
