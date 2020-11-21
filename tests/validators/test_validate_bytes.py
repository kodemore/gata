from base64 import b64encode

import pytest

from gata.errors import ValidationError
from gata.validators import validate_bytes


@pytest.mark.parametrize(
    "value",
    [b64encode(b"asa"), b64encode(b"another"), b"some bytes", bytearray(b"byte array")],
)
def test_valid_values(value: str):
    assert validate_bytes(value)


@pytest.mark.parametrize("value", ["asa", "another", 1])
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_bytes(value)
