from base64 import b64encode
from datetime import date
from datetime import datetime
from enum import Enum
from typing import List
from typing import Union

import pytest

from gata import DataClass
from gata import types
from gata.dataclass import serialise_value
from gata.dataclass import unserialise_value


# Fixtures
class EnumFixture(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class DataClassFixture(DataClass):
    name: str = "John"
    age: int
    favourites: Union[int, str, float]

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class PetStatus(Enum):
    AVAILABLE = 0
    SOLD = 1
    RESERVED = 2


class Favourite(DataClass):
    name: str
    priority: int = 0

    def __init__(self, name: str):
        self.name = name


class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    favourites: List[Favourite]
    status: PetStatus = PetStatus.AVAILABLE
    created_at: datetime

    def __init__(self, name: str, age: int, favourites: List[Favourite], status: PetStatus):
        self.name = name
        self.age = age
        self.favourites = favourites
        self.status = status
        self.created_at = datetime.now()


@pytest.mark.parametrize(
    "schema,value,expected",
    [
        # formatted strings
        (types.String[types.Format.BYTE], b64encode(b"test"), b"test"),
        (
            types.String[types.Format.DATE],
            "2019-10-11",
            date(year=2019, month=10, day=11),
        ),
        (
            types.String[types.Format.DATETIME],
            "2019-10-11 11:11:11",
            datetime(year=2019, month=10, day=11, hour=11, minute=11, second=11),
        ),
        (types.Number, 10e5, 1000000.0),
        (types.Array[types.Integer], (1, 2, 3), [1, 2, 3]),
        (types.Boolean, True, True),
        (types.Enum([1, 2, 3], EnumFixture), 1, EnumFixture.ONE),
        (types.Enum([1, 2, 3]), 1, 1),
    ],
)
def test_unserialise_value(schema, value, expected) -> None:
    assert unserialise_value(schema, value) == expected


@pytest.mark.parametrize(
    "schema,value,expected",
    [
        (types.String[types.Format.BYTE], b"test", b64encode(b"test").decode("utf8")),
        (
            types.String[types.Format.DATETIME],
            datetime(year=2019, month=10, day=11, hour=11, minute=11, second=11),
            "2019-10-11T11:11:11",
        ),
        (types.Array[types.Integer], (1, 2, 3), [1, 2, 3]),
        (types.Enum([1, 2, 3]), EnumFixture.ONE, 1),
    ],
)
def test_serialize_value(schema, value, expected) -> None:
    assert serialise_value(schema, value) == expected


def test_can_define_class() -> None:
    assert issubclass(DataClassFixture, DataClass)
    assert hasattr(DataClassFixture, "validate")
    assert hasattr(DataClassFixture, "create")
    assert hasattr(DataClassFixture, "__dataclass__")


def test_can_create_instance_from_data_class() -> None:

    roxy = Pet.create({"name": "Roxy"})
    rex = Pet.create({"name": "Rex", "age": 10})

    assert isinstance(roxy, Pet)
    assert isinstance(roxy, DataClass)
    assert roxy.name == "Roxy"
    assert roxy.age == 0
    assert roxy.favourites is None

    assert isinstance(rex, Pet)
    assert isinstance(rex, DataClass)
    assert rex.name == "Rex"
    assert rex.age == 10
    assert roxy.favourites == None


def test_can_unserialise_nested_instance_from_data_classes() -> None:
    roxy = Pet.create(
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


def test_can_serialise_complex_object() -> None:
    favourite_list = [
        Favourite("bones"),
        Favourite("ball"),
    ]

    doggo = Pet("Doggo", 10, favourite_list, PetStatus.SOLD)

    assert doggo.serialise() == {
        "name": "Doggo",
        "age": 10,
        "favourites": [
            {"name": "bones", "priority": 0},
            {"name": "ball", "priority": 0},
        ],
        "status": 1,
        "created_at": doggo.created_at.isoformat()
    }


def test_override_base_methods() -> None:

    class PetWithHooks(DataClass):
        name: str = "Doggo"
        age: int = 0
        favourites: List[Favourite]
        status: PetStatus = PetStatus.AVAILABLE
        created_at: datetime

        def create(cls, properties: dict) -> "DataClass":
            return super().create(cls, properties)

        def serialise(self) -> dict:
            return super().serialise()

    raw_doggo = {
        "name": "Doggo",
        "favourites": [{"name": "ball", "priority": 10}, {"name": "bone"}],
        "status": 2,
        "created_at": "2016-09-18T17:34:02.666Z",
    }

    doggo_instance = PetWithHooks.create(raw_doggo)
    assert doggo_instance.serialise() == {
        'age': 0,
        'created_at': '2016-09-18T17:34:02+00:00',
        'favourites': [
            {'name': 'ball', 'priority': 10},
            {'name': 'bone', 'priority': 0},
        ],
        'name': 'Doggo',
        'status': 2,
    }
