import pytest

from gata.errors import ValidationError
from gata.validators import validate_enum
from enum import Enum


@pytest.mark.parametrize("input", ["test_a", "test_b", "test_c"])
def test_validate_valid_enum(input: str):
    class TestEnum(Enum):
        TEST_A = "test_a"
        TEST_B = "test_b"
        TEST_C = "test_c"

    assert validate_enum(input, TestEnum)


@pytest.mark.parametrize("input", ["e", "f", "g", 1, 2])
def test_validate_invalid_enum(input: str):
    class TestEnum(Enum):
        TEST_A = "test_a"
        TEST_B = "test_b"
        TEST_C = "test_c"

    with pytest.raises(ValidationError):
        validate_enum(input, TestEnum)
