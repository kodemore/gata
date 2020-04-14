import pytest

from gata.errors import ValidationError
from gata.validators import validate_boolean


@pytest.mark.parametrize("input", [True, False, 1, "t", "f", "false", "true", "on", "off"])
def test_validate_valid_boolean(input: str):
    assert validate_boolean(input) is not None


@pytest.mark.parametrize("input", [-1, "any", "ni"])
def test_validate_invalid_boolean(input: str):
    with pytest.raises(ValidationError):
        validate_boolean(input)
