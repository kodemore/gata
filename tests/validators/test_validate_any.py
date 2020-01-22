import pytest

from gata.validators import validate_any, validate_integer, validate_string


def test_valid_any():
    assert validate_any("2019-10-10 10:10:10", (validate_string, validate_integer),)

    with pytest.raises(ValueError):
        validate_any(False, (validate_string, validate_integer))
