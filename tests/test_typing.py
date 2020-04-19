from dataclasses import field
from typing import Optional

from gata import typing, dataclass


def test_gata_types() -> None:
    @dataclass
    class BoJack:
        name: str
        address: typing.EmailAddress
        webpage: typing.UrlAddress
        birth_date: Optional[typing.Date] = field(default=None)
        joined: Optional[typing.DateTime] = field(default=None)
        online_time: Optional[typing.Duration] = field(default=None)

    assert BoJack.validate(
        {
            "name": "Jack",
            "address": "bo@jack.com",
            "webpage": "http://www.boo-jack.com",
            "birth_date": "1970-01-01",
            "joined": "1970-01-01 10:12:12",
            "online_time": "P300D",
        }
    )

    try:
        BoJack(name="Jack", address="error", webpage="http://www.boo-jack.com")
    except ValueError as error:

        assert error.code == "field_error"
        assert error.caused_by.code == "format_error"
        assert error.context["field_name"] == "address"

    bojack = BoJack(
        **{
            "name": "Jack",
            "address": "bo@jack.com",
            "webpage": "http://www.boo-jack.com",
            "birth_date": "1970-01-01",
            "joined": "1970-01-01 10:12:12",
            "online_time": "P300D",
        }
    )

    assert isinstance(bojack, BoJack)

    assert bojack.serialise() == {
        "address": "bo@jack.com",
        "birth_date": "1970-01-01",
        "joined": "1970-01-01T10:12:12",
        "name": "Jack",
        "online_time": "P42W6D",
        "webpage": "http://www.boo-jack.com",
    }
