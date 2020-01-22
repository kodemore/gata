import pytest
from typing_extensions import Literal

from gata.errors import ValidationError
from gata.validators import validate_literal


def test_valid_values():
    assert validate_literal(1, Literal[1, "2", "a"])


def test_invalid_values():
    with pytest.raises(ValidationError):
        validate_literal(None, Literal[1, "2", "a"])

    with pytest.raises(ValidationError):
        validate_literal(2, Literal[1, "2", "a"])
