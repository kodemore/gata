from datetime import datetime
from enum import Enum
from typing import List

from gata import DataClass
from gata.errors import FieldError


class PetStatus(Enum):
    AVAILABLE = 0
    SOLD = 1
    RESERVED = 2


class Favourite(DataClass):
    name: str
    priority: int = 0


class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    favourites: List[Favourite]
    tags: List[str]
    status: PetStatus = PetStatus.AVAILABLE
    created_at: datetime

    class Meta:
        tags = {"items": {"min": 2, "max": 10}}
        name = {"min": 2, "max": 20}
        age = {"min": 0, "max": 100}

    def __init__(self, name: str = "Pimpek", age: int = 0):
        self.name = name
        self.favourites = []
        self.tags = []
        self.age = age


def test_validate_data_with_dataclass() -> None:
    try:
        Pet.validate({"age": 120})
    except FieldError as error:
        assert error.field_name == "age"


def test_unserialise_dataclass() -> None:
    pet = Pet.unserialise(
        {
            "name": "Tom",
            "age": 10,
            "favourites": [{"name": "bones"}, {"name": "sousage"}],
            "status": 1,
            "created_at": "2020-01-01 10:10:10",
        }
    )

    assert isinstance(pet, Pet)
    assert isinstance(pet.favourites[0], Favourite)
    assert isinstance(pet.created_at, datetime)


def test_serialise_dataclass() -> None:
    pet = Pet("Boo", 20)
    assert pet.serialise() == {
        "name": "Boo",
        "age": 20,
        "favourites": [],
        "tags": [],
        "status": 0,
        "created_at": None,
    }
