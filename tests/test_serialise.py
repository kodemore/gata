from datetime import date
from datetime import datetime
from datetime import time
from typing import List, Set

from gata.serialise import serialise
from tests.fixtures import Favourite
from tests.fixtures import PetStatus


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


def test_serialise_dataclass_instance() -> None:
    assert serialise(Favourite("test", 2), Favourite) == {"name": "test", "priority": 2}


def test_serialise_null() -> None:
    assert serialise(None, int) is None
    assert serialise(None, str) is None
    assert serialise(None, bool) is None
    assert serialise(None, float) is None
    assert serialise(None, datetime) is None
    assert serialise(None, date) is None
    assert serialise(None, time) is None
    assert serialise(None, Set[str]) == {}
    assert serialise(None, List[str]) == []


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
    assert serialise({"a", "b", "c"}, Set[str]) == {"a", "b", "c"}
    assert serialise(
        {
            date(year=2019, month=1, day=20),
            date(year=2019, month=2, day=20),
            date(year=2019, month=3, day=20),
        },
        Set[date],
    ) == {"2019-01-20", "2019-02-20", "2019-03-20"}
