import pytest

from gata.errors import ValidationError
from gata.types import Number


def test_can_instantiate():
    schema = Number()
    assert schema.validate(10.12) is None


@pytest.mark.parametrize("value", (None, "", "10", False, True))
def test_validation_fail(value):
    with pytest.raises(ValidationError):
        validator = Number(nullable=False)
        validator.validate(value)


@pytest.mark.parametrize("value", (0, 1, -1, 2.13, 200000, 2j + 10))
def test_validation_pass(value):
    assert Number().validate(value) is None


@pytest.mark.parametrize("multiplication,value", ((2, 8), (3, 6), (1, 21), (-2, -8)))
def test_pass_multiple_of(multiplication, value):
    assert Number(multiple_of=multiplication).validate(value) is None


@pytest.mark.parametrize("multiplication,value", ((2, 7), (3, 4), (-2, 9)))
def test_fail_multiple_of(multiplication, value):
    with pytest.raises(ValidationError):
        Number(multiple_of=multiplication).validate(value)


@pytest.mark.parametrize(
    "min,max,value",
    ((2, 8.1, 8.01), (3, None, 6), (None, 21.1, 21), (-2, 0, -1), (2, 4, 3)),
)
def test_pass_range(min, max, value):
    assert Number(minimum=min, maximum=max).validate(value) is None


@pytest.mark.parametrize(
    "min,max,value", ((2, 10, 1), (3, None, 2), (None, 21, 22), (-2, 0, 1))
)
def test_fail_range(min, max, value):
    with pytest.raises(ValidationError):
        Number(minimum=min, maximum=max).validate(value)


def test_nullable():
    assert Number(nullable=True).validate(None) is None
