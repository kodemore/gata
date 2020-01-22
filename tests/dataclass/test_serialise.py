from datetime import date, datetime, time
from typing import Any, FrozenSet, List, Set, Tuple

import pytest
from typing_extensions import Literal

from gata.dataclass.serialise import serialise
from gata.errors import SerialisationError
from tests.fixtures import Favourite, Pet, PetDict, PetStatus


def test_serialise_enums() -> None:
    assert serialise(PetStatus.AVAILABLE, PetStatus) == 0


def test_serialise_int() -> None:
    assert serialise("2", int) == 2
    assert serialise(1, int) == 1
    assert serialise(3.1, int) == 3


def test_serialise_float() -> None:
    assert serialise("2.1", float) == 2.1
    assert serialise(1, float) == 1.0
    assert serialise(3.1, float) == 3.1


def test_serialise_bool() -> None:
    assert serialise("1", bool) is True
    assert serialise("", bool) is False
    assert serialise(True, bool) is True
    assert serialise(False, bool) is False


def test_serialise_datetime() -> None:
    assert (
        serialise(
            datetime(year=2019, month=1, day=1, hour=13, minute=2, second=1), datetime
        )
        == "2019-01-01T13:02:01"
    )


def test_serialise_date() -> None:
    assert serialise(date(year=2019, month=1, day=20), date) == "2019-01-20"


def test_serialise_time() -> None:
    assert serialise(time(hour=13, minute=2, second=1), time) == "13:02:01"


def test_serialise_string() -> None:
    assert serialise(1, str) == "1"
    assert serialise("test", str) == "test"


def test_serialise_null() -> None:
    assert serialise(None, int) is None
    assert serialise(None, str) is None
    assert serialise(None, bool) is None
    assert serialise(None, float) is None
    assert serialise(None, datetime) is None
    assert serialise(None, date) is None
    assert serialise(None, time) is None
    assert serialise(None, Set[str]) == []
    assert serialise(None, List[str]) == []


def test_serialise_tuple() -> None:
    assert serialise(("a", "1", "t"), Tuple[str, int, bool]) == ["a", 1, True]


def test_serialise_list() -> None:
    assert serialise(["a", "b", "c"], List[str]) == ["a", "b", "c"]
    assert serialise(
        [
            date(year=2019, month=1, day=20),
            date(year=2019, month=2, day=20),
            date(year=2019, month=3, day=20),
        ],
        List[date],
    ) == ["2019-01-20", "2019-02-20", "2019-03-20"]
    assert serialise(None, List[str]) == []


def test_serialise_set() -> None:
    serialised_set = serialise({"a", "b", "c"}, Set[str])
    assert isinstance(serialised_set, list)
    assert len(serialised_set) == 3
    assert "a" in serialised_set
    assert "b" in serialised_set
    assert "c" in serialised_set

    serialised_dates = serialise(
        {
            date(year=2019, month=1, day=20),
            date(year=2019, month=2, day=20),
            date(year=2019, month=3, day=20),
        },
        Set[date],
    )
    assert isinstance(serialised_set, list)
    assert len(serialised_set) == 3
    assert "2019-01-20" in serialised_dates
    assert "2019-02-20" in serialised_dates
    assert "2019-03-20" in serialised_dates


def test_fail_serialise_generic_list() -> None:
    with pytest.raises(SerialisationError):
        serialise([1, 2, 3], list)

    with pytest.raises(SerialisationError):
        serialise([1, 2, 3], List)


def test_fail_serialise_generic_set() -> None:
    with pytest.raises(SerialisationError):
        serialise({1, 2, 3}, set)

    with pytest.raises(SerialisationError):
        serialise({1, 2, 3}, Set)


def test_fail_serialise_generic_tuple() -> None:
    with pytest.raises(SerialisationError):
        serialise((1, 2, 3), tuple)

    with pytest.raises(SerialisationError):
        serialise((1, 2, 3), Tuple)


def test_fail_serialise_any() -> None:
    with pytest.raises(SerialisationError):
        serialise(1, Any)


def test_serialise_dataclass() -> None:
    assert serialise(Favourite("Test Name", 12), Favourite) == {
        "name": "Test Name",
        "priority": 12,
    }


def test_serialise_frozenset() -> None:
    assert serialise([1, 2, 3], FrozenSet[int]) == [1, 2, 3]


def test_serialise_complex_dataclass() -> None:
    pet = Pet(name="Pimpek", favourites=[Favourite("fav_1"), Favourite("fav_2")])

    result = serialise(pet, Pet)

    assert result["name"] == "Pimpek"
    assert result["tags"] == []
    assert result["favourites"] == [
        {"name": "fav_1", "priority": 0},
        {"name": "fav_2", "priority": 0},
    ]
    assert result["status"] == 0


def test_serialise_literal() -> None:
    serialise(1, Literal[1, "a", True])


def test_serialise_typed_dict() -> None:
    serialise(PetDict(tags=["a", "b", "c"], name="Pimpek", age=10), PetDict)