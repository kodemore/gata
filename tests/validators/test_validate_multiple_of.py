import pytest

from gata.validators import validate_multiple_of


@pytest.mark.parametrize(
    "value,multiple_of", ((2, 1), (9, 3), (12.0, 4.0), (1, 1), (64, 8.0),),
)
def test_pass_validation(value, multiple_of: float):
    assert validate_multiple_of(value, multiple_of)


@pytest.mark.parametrize(
    "value,multiple_of", ((2, 3), (5, 3), (7, 3),),
)
def test_fail_validation(value, multiple_of):
    with pytest.raises(ValueError):
        assert validate_multiple_of(value, multiple_of)
