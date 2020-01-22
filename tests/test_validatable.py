from dataclasses import dataclass
from typing import List

import pytest

from gata import validatable
from tests.fixtures import Favourite, PetStatus


def test_validatable() -> None:
    @validatable()
    @dataclass()
    class ValidatablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    assert ValidatablePet(name="BoJack", status=PetStatus.AVAILABLE, favourites=[])
    assert hasattr(ValidatablePet, "validate")

    with pytest.raises(ValueError):
        ValidatablePet(name="BoJack", status=10, favourites=[])

    assert ValidatablePet.validate({"name": "BoJack", "status": 0, "favourites": []})


def test_validatable_decorator_without_calling_it() -> None:
    @validatable
    @dataclass()
    class ValidatablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    assert hasattr(ValidatablePet, "validate")
