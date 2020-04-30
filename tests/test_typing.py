from dataclasses import field, dataclass
from typing import Optional, List

from gata import typing, dataclass
from gata.schema import Field
from gata.schema import Format


def test_create_validator_from_type() -> None:
    duration = typing.Duration

    validate = duration.validate

    validate(object(), "P2D")
    a = 1


def test_constrained_list() -> None:
    @dataclass
    class ExampleList:
        adresses: List[str] = Field(items=Field(string_format=Format.EMAIL))
