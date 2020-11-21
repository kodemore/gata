import pytest

from gata.validators import validate_frozenset, validate_integer


def test_validate_frozenset():
    assert validate_frozenset(
        {"2019-10-10 10:10:10", "2019-10-10 10:10:10", "2019-10-10 10:10:10"}
    )

    with pytest.raises(ValueError):
        validate_frozenset(1)

    with pytest.raises(ValueError):
        validate_frozenset("a")

    assert validate_frozenset({1, 2, 3}, validate_integer)

    assert validate_frozenset([1, 2, 3]) == frozenset([1, 2, 3])
