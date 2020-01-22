from dataclasses import dataclass
from typing import List

import pytest

from gata import serialisable
from tests.fixtures import Favourite, PetStatus


def test_serialisable_decorator():
    @serialisable()
    @dataclass()
    class SerialisablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    pet = SerialisablePet(
        name="Tom", status=PetStatus.AVAILABLE, favourites=[Favourite("bone")]
    )

    assert hasattr(pet, "serialise")
    assert pet.serialise() == {
        "favourites": [{"name": "bone", "priority": 0}],
        "name": "Tom",
        "status": 0,
    }

    assert hasattr(SerialisablePet, "deserialise")
    deserialised_tom = SerialisablePet.deserialise(
        {"favourites": [{"name": "bone", "priority": 0}], "name": "Tom", "status": 0,}
    )

    assert isinstance(deserialised_tom, SerialisablePet)
    assert isinstance(deserialised_tom.favourites[0], Favourite)
    assert deserialised_tom.name == "Tom"
    assert deserialised_tom.status is PetStatus.AVAILABLE


def test_fail_when_decorate_non_dataclass() -> None:

    with pytest.raises(AssertionError):

        @serialisable()
        class SomeClass:
            pass


def test_decorator_without_calling_it() -> None:
    @serialisable
    @dataclass()
    class SerialisablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    pet = SerialisablePet(
        name="Tom", status=PetStatus.AVAILABLE, favourites=[Favourite("bone")]
    )
    assert pet.serialise() == {
        "favourites": [{"name": "bone", "priority": 0}],
        "name": "Tom",
        "status": 0,
    }
