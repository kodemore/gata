import pytest
from gata.validators import validate_boolean
from gata.errors import ValidationError


@pytest.mark.parametrize("input", [True, False])
def test_validate_valid_boolean(input: str):
    assert validate_boolean(input)


@pytest.mark.parametrize("input", [1, 1.0, "1", "any", "ni"])
def test_validate_invalid_boolean(input: str):
    with pytest.raises(ValidationError):
        validate_boolean(input)
