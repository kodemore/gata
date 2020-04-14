import pytest

from gata.validators import validate_iterable


def test_valid_array():
    assert validate_iterable(["2019-10-10 10:10:10", "2019-10-10 10:10:10", "2019-10-10 10:10:10"])

    with pytest.raises(ValueError):
        validate_iterable(1)

    with pytest.raises(ValueError):
        validate_iterable("a")
