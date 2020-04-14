import pytest

from gata.errors import BoundValidationError
from gata.validators import validate_range


@pytest.mark.parametrize(
    "min_len,max_len,value", ((2, 10, 3), (1, 2, 2), (1, 2, 1), (None, 3, 3), (2, None, 4)),
)
def test_pass_validation(min_len, max_len, value):
    assert validate_range(value, minimum=min_len, maximum=max_len)


@pytest.mark.parametrize(
    "min_len,max_len,value", ((2, 10, 1), (1, 2, 3), (1, 2, 0), (None, 3, 4), (2, None, 1)),
)
def test_fail_validation(min_len, max_len, value):
    with pytest.raises(BoundValidationError):
        assert validate_range(value, minimum=min_len, maximum=max_len)
