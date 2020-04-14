import pytest
from typing import Any
from gata.validators import validate_string


@pytest.mark.parametrize("value", ("17:34:02.124Z", "17:34:02.124Z", "17:34:02", "17:34:02.124"))
def test_valid_values(value: str) -> None:
    assert validate_string(value)


@pytest.mark.parametrize("value", (1, True, None))
def test_invalid_values(value: Any) -> None:
    with pytest.raises(ValueError):
        validate_string(value)
