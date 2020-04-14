import pytest

from gata.errors import ValidationError
from gata.validators import validate_semver


@pytest.mark.parametrize("value", ("1.0.0", "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-0.3.7", "1.0.0-x.7.z.92"))
def test_valid_values(value: str):
    assert validate_semver(value) == value


@pytest.mark.parametrize(
    "value", ("1", "1.0", "1.0.0-.123", "1.0.0-...", "1.0.0-123.", "1.0.0-+", "1.0.0-+123", "1.0.0-")
)
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        assert validate_semver(value)
