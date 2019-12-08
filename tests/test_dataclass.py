from gata import DataClass
from typing import Union
from typing import List
from enum import Enum
from datetime import datetime


def test_can_define_class() -> None:
    class Example(DataClass):
        name: str = "John"
        age: int
        favourites: Union[int, str, float]

    assert issubclass(Example, DataClass)
    assert hasattr(Example, "validate")
    assert hasattr(Example, "unserialise")
    assert hasattr(Example, "__dataclass__")


def test_can_create_instance_from_data_class() -> None:
    class Pet(DataClass):
        name: str = "Pimpek"
        age: int = 0
        favourites: List[str] = ["bone", "ball"]

    roxy = Pet.unserialise({"name": "Roxy"})
    rex = Pet.unserialise({"name": "Rex", "age": 10})

    assert isinstance(roxy, Pet)
    assert isinstance(roxy, DataClass)
    assert roxy.name == "Roxy"
    assert roxy.age == 0
    assert roxy.favourites == ["bone", "ball"]

    assert isinstance(rex, Pet)
    assert isinstance(rex, DataClass)
    assert rex.name == "Rex"
    assert rex.age == 10
    assert roxy.favourites == ["bone", "ball"]


def test_can_create_nested_instance_from_data_classes() -> None:
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
        status: PetStatus = PetStatus.AVAILABLE
        created_at: datetime

    roxy = Pet.unserialise(
        {
            "name": "Roxy",
            "favourites": [{"name": "ball", "priority": 10}, {"name": "bone"}],
            "status": 2,
            "created_at": "2016-09-18T17:34:02.666Z",
        }
    )
    assert isinstance(roxy, Pet)
    assert isinstance(roxy, DataClass)
    assert isinstance(roxy.status, PetStatus)
    assert isinstance(roxy.favourites[0], Favourite)
    assert isinstance(roxy.favourites[1], Favourite)
    assert isinstance(roxy.created_at, datetime)

    assert roxy.favourites[0].name == "ball"
    assert roxy.favourites[0].priority == 10
    assert roxy.favourites[1].name == "bone"
    assert roxy.favourites[1].priority == 0
