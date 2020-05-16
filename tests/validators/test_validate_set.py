import pytest

from gata.validators import validate_set, validate_integer


def test_validate_set():
    assert validate_set({"2019-10-10 10:10:10", "2019-10-10 10:10:10", "2019-10-10 10:10:10"})

    with pytest.raises(ValueError):
        validate_set(1)

    with pytest.raises(ValueError):
        validate_set("a")

    assert validate_set({1, 2, 3}, validate_integer)

    assert validate_set([1, 2, 3]) == {1, 2, 3}
