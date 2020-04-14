from ipaddress import IPv4Address

import pytest

from gata.errors import ValidationError
from gata.validators import validate_ipv4


@pytest.mark.parametrize("value", ("0.0.0.0", "127.0.0.1"))
def test_valid_values(value: str):
    assert isinstance(validate_ipv4(value), IPv4Address)


@pytest.mark.parametrize("value", ("1200::AB00:1234::2552:7777:1313", "1200:0000:AB00:1234:O000:2552:7777:1313"))
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_ipv4(value)
