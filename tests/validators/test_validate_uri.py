import pytest

from gata.errors import ValidationError
from gata.validators import validate_uri


@pytest.mark.parametrize(
    "value",
    (
        "http://foo.com/blah_blah",
        "http://foo.com/blah_blah/",
        "https://www.example.com/foo/?bar=baz&inga=42&quux",
        "http://userid:password@example.com",
        "http://142.42.1.1:8080/",
        "http://142.42.1.1/",
        "http://code.google.com/events/#&product=browser",
        "http://a.b-c.de",
        "https://foo_bar.example.com/",
        "http://jabber.tcp.gmail.com",
        "http://_jabber._tcp.gmail.com",
        "http://مثال.إختبار",
    ),
)
def test_validate_uri_valid_values(value: str):
    assert validate_uri(value)


@pytest.mark.parametrize(
    "value", ("aaaa", "...", "####/3s"),
)
def test_validate_uri_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_uri(value)
