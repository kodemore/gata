from functools import partial

import pytest

from gata.validators import validate_all
from gata.validators import validate_format
from gata.validators import validate_integer
from gata.validators import validate_string


def test_valid_all():
    assert validate_all(
        "2019-10-10 10:10:10",
        (validate_string, partial(validate_format, format="datetime")),
    )

    with pytest.raises(ValueError):
        validate_all(1, (validate_string, validate_integer))
