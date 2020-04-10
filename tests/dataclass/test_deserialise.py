from datetime import date, datetime, time
from typing import FrozenSet, List, Set, Tuple, Optional, Union
from dataclasses import dataclass
from decimal import Decimal
import pytest

from gata.errors import DeserialisationError
from gata.dataclass.deserialise import deserialise
from tests.fixtures import Favourite, Pet, PetDict, PetStatus, PetWithVirtualProperties
from bson import ObjectId


def test_deserialise_enums() -> None:
    assert deserialise(0, PetStatus) == PetStatus.AVAILABLE


def test_deserialise_int() -> None:
    assert deserialise("2", int) == 2
    assert deserialise(1, int) == 1
    assert deserialise(3.1, int) == 3


def test_deserialise_float() -> None:
    assert deserialise("2.1", float) == 2.1
    assert deserialise(1, float) == 1.0
    assert deserialise(3.1, float) == 3.1


def test_deserialise_bool() -> None:
    assert deserialise("1", bool) is True
    assert deserialise("", bool) is False
    assert deserialise(True, bool) is True
    assert deserialise(False, bool) is False


def test_deserialise_datetime() -> None:
    assert deserialise("2019-01-01T13:02:01", datetime) == datetime(
        year=2019, month=1, day=1, hour=13, minute=2, second=1
    )

    assert deserialise(datetime(2019, 1, 1, 1, 1, 1), datetime) == datetime(
        2019, 1, 1, 1, 1, 1
    )


def test_deserialise_date() -> None:
    assert deserialise("2019-01-20", date) == date(year=2019, month=1, day=20)
    assert deserialise(date(year=2019, month=1, day=20), date) == date(
        year=2019, month=1, day=20
    )


def test_deserialise_object_id() -> None:
    example_id = ObjectId()
    assert deserialise(str(example_id), ObjectId) == example_id


def test_deserialise_time() -> None:
    assert deserialise("13:02:01", time) == time(hour=13, minute=2, second=1)


def test_deserialise_string() -> None:
    assert deserialise(1, str) == "1"
    assert deserialise("test", str) == "test"


def test_deserialise_null() -> None:
    assert deserialise(None, int) is None
    assert deserialise(None, str) is None
    assert deserialise(None, bool) is None
    assert deserialise(None, float) is None
    assert deserialise(None, datetime) is None
    assert deserialise(None, date) is None
    assert deserialise(None, time) is None
    assert deserialise(None, List[str]) == []
    assert deserialise(None, Set[str]) == set()
    assert deserialise(None, FrozenSet[str]) == frozenset()
    assert deserialise(None, Tuple[str]) == tuple()


def test_deserialise_tuple() -> None:
    assert deserialise([1, 2, 3], Tuple[int, ...]) == tuple([1, 2, 3])
    assert deserialise([1, 2, 3], Tuple[int, str]) == tuple([1, "2"])


def test_fail_deserialise_gerneric_tuple() -> None:
    with pytest.raises(DeserialisationError):
        deserialise([1, 2, 3], Tuple)


def test_deserialise_list() -> None:
    assert deserialise(["a", "b", "c"], List[str]) == ["a", "b", "c"]
    assert deserialise(["2019-01-20", "2019-02-20", "2019-03-20"], List[date]) == [
        date(year=2019, month=1, day=20),
        date(year=2019, month=2, day=20),
        date(year=2019, month=3, day=20),
    ]


def test_deserialise_set() -> None:
    assert deserialise(["a", "b", "c"], Set[str]) == {"a", "b", "c"}
    assert deserialise(["2019-01-20", "2019-02-20", "2019-03-20"], Set[date]) == {
        date(year=2019, month=1, day=20),
        date(year=2019, month=2, day=20),
        date(year=2019, month=3, day=20),
    }


def test_deserialise_frozenset() -> None:
    assert deserialise(["a", "b", "c"], FrozenSet[str]) == {"a", "b", "c"}


def test_deserialise_dataclass_instance() -> None:
    pet = deserialise(
        {
            "favourites": [{"name": "test", "priority": 2}],
            "name": "Pimpek",
            "status": 1,
        },
        Pet,
    )
    assert isinstance(pet, Pet)
    assert isinstance(pet.favourites[0], Favourite)


def test_deserialise_typed_dict() -> None:
    pet = deserialise({"tags": ["tag_a", "tag_b"], "name": "Pimpek"}, PetDict)

    assert pet["tags"] == ["tag_a", "tag_b"]
    assert pet["name"] == "Pimpek"


@pytest.mark.parametrize(
    "value,type_definition,expected",
    [
        [None, Optional[int], None],
        [None, Optional[str], None],
        ["a", Union[int, str], "a"],
        [1, Optional[int], 1],
        ["a", Optional[str], "a"],
        [None, Optional[datetime], None],
        ["2020-01-01", Optional[date], date(2020, 1, 1)],
        ["21.123", Union[Decimal, float], Decimal("21.123")],
        ["21.123", Union[float, Decimal], 21.123],
    ],
)
def test_deserialise_union_primitive_types(value, type_definition, expected) -> None:
    assert deserialise(value, type_definition) == expected


def test_deserialise_union_dataclasses() -> None:
    @dataclass()
    class Animal:
        age: int
        group: str

    @dataclass()
    class Dog(Animal):
        legs: int

    @dataclass()
    class Fish(Animal):
        fins: int

    assert isinstance(
        deserialise(
            {"age": 10, "group": "fishes", "fins": 2}, Union[Dog, Fish, Animal]
        ),
        Fish,
    )
    assert isinstance(
        deserialise(
            {"age": 10, "group": "fishes", "legs": 2}, Union[Dog, Fish, Animal]
        ),
        Dog,
    )
    assert isinstance(
        deserialise({"group": "fishes", "age": 10}, Union[Dog, Fish, Animal]), Animal
    )


def test_read_only_property() -> None:
    pet = deserialise({"name": "Boo", "favourite_id": 2}, PetWithVirtualProperties)

    assert isinstance(pet, PetWithVirtualProperties)
    assert pet.name == "Boo"
    assert pet.favourite_id == 2


def test_deserialise_with_user_defined_deserialiser() -> None:
    @dataclass
    class PetWithDeserialiser:
        name: str
        status: PetStatus
        favourites: list

        class Meta:
            @staticmethod
            def deserialise_favourites(favourites: List[str]) -> List[Favourite]:
                return [Favourite(name=favourite) for favourite in favourites]

    pet = deserialise(
        {"name": "Boo", "status": 0, "favourites": ["bone", "candy"]},
        PetWithDeserialiser,
    )

    assert len(pet.favourites) == 2
    for favourite in pet.favourites:
        assert isinstance(favourite, Favourite)
    assert pet.name == "Boo"
