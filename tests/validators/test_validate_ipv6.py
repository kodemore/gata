from ipaddress import IPv6Address

import pytest

from gata.errors import ValidationError
from gata.validators import validate_ipv6


@pytest.mark.parametrize("value", ("1200:0000:AB00:1234:0000:2552:7777:1313", "21DA:D3:0:2F3B:2AA:FF:FE28:9C5A"))
def test_valid_values(value: str):
    assert isinstance(validate_ipv6(value), IPv6Address)


@pytest.mark.parametrize("value", ("1200::AB00:1234::2552:7777:1313", "1200:0000:AB00:1234:O000:2552:7777:1313"))
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_ipv6(value)
