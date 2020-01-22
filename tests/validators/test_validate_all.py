import pytest

from gata.validators import (
    validate_all,
    validate_datetime,
    validate_integer,
    validate_string,
)


def test_valid_all():
    assert validate_all("2019-10-10 10:10:10", (validate_string, validate_datetime),)

    with pytest.raises(ValueError):
        validate_all(1, (validate_string, validate_integer))
