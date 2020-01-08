import pytest
from gata.validators import validate_truthy
from gata.errors import ValidationError


@pytest.mark.parametrize("input", ["1", "true", "yes", "y", "yup", "on"])
def test_validate_valid_truthy(input: str):
    assert validate_truthy(input)


@pytest.mark.parametrize("input", ["0", "any", "ni"])
def test_validate_invalid_truthy(input: str):
    with pytest.raises(ValidationError):
        validate_truthy(input)
