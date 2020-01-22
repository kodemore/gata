from dataclasses import dataclass, field
from typing import Optional

from gata import typing, validatable


def test_gata_types() -> None:
    @validatable
    @dataclass()
    class BoJack:
        name: str
        address: typing.EmailAddress
        webpage: typing.UrlAddress
        birth_date: Optional[typing.Date] = field(default=None)

    assert BoJack.validate(
        {
            "name": "Jack",
            "address": "bo@jack.com",
            "webpage": "http://www.boo-jack.com",
            "birth_date": "1970-01-01",
        }
    )

    try:
        BoJack(name="Jack", address="error", webpage="http://www.boo-jack.com")
    except ValueError as error:

        assert error.code == "field_error"
        assert error.caused_by.code == "format_error"
        assert error.context["field_name"] == "address"
