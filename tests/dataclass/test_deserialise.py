from datetime import date, datetime, time
from typing import FrozenSet, List, Set, Tuple

from gata.dataclass.deserialise import deserialise
from tests.fixtures import Favourite, Pet, PetDict, PetStatus


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


def test_deserialise_date() -> None:
    assert deserialise("2019-01-20", date) == date(year=2019, month=1, day=20)


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
