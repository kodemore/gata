from functools import partial

import pytest

from gata.validators import validate_array
from gata.validators import validate_format
from gata.validators import validate_integer


def test_valid_array():
    assert validate_array(
        ["2019-10-10 10:10:10", "2019-10-10 10:10:10", "2019-10-10 10:10:10"],
        partial(validate_format, format="datetime"),
    )

    with pytest.raises(ValueError):
        validate_array(1, validate_integer)

    with pytest.raises(ValueError):
        validate_array(["a"], validate_integer)
