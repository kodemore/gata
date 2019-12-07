from gata.types import *
import pytest
from gata.errors import ValidationError


def test_validate_null() -> None:
    null_validator = Null
    null_validator.validate(None)


def test_fail_validate_null() -> None:
    null_validator = Null
    with pytest.raises(ValidationError):
        null_validator.validate(1)
