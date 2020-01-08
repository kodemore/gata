from datetime import date
from datetime import datetime
from datetime import time
from typing import List, Set

from gata.unserialise import unserialise
from tests.fixtures import Favourite
from tests.fixtures import PetStatus


def test_unserialise_enums() -> None:
    assert unserialise(0, PetStatus) == PetStatus.AVAILABLE


def test_unserialise_int() -> None:
    assert unserialise("2", int) == 2
    assert unserialise(1, int) == 1
    assert unserialise(3.1, int) == 3


def test_unserialise_float() -> None:
    assert unserialise("2.1", float) == 2.1
    assert unserialise(1, float) == 1.0
    assert unserialise(3.1, float) == 3.1


def test_unserialise_bool() -> None:
    assert unserialise("1", bool) is True
    assert unserialise("", bool) is False
    assert unserialise(True, bool) is True
    assert unserialise(False, bool) is False


def test_unserialise_datetime() -> None:
    assert unserialise("2019-01-01T13:02:01", datetime) == datetime(
        year=2019, month=1, day=1, hour=13, minute=2, second=1
    )


def test_unserialise_date() -> None:
    assert unserialise("2019-01-20", date) == date(year=2019, month=1, day=20)


def test_unserialise_time() -> None:
    assert unserialise("13:02:01", time) == time(hour=13, minute=2, second=1)


def test_unserialise_string() -> None:
    assert unserialise(1, str) == "1"
    assert unserialise("test", str) == "test"


def test_unserialise_dataclass_instance() -> None:
    favourite = unserialise({"name": "test", "priority": 2}, Favourite)
    assert isinstance(favourite, Favourite)
    assert favourite.name == "test"
    assert favourite.priority == 2


def test_unserialise_null() -> None:
    assert unserialise(None, int) is None
    assert unserialise(None, str) is None
    assert unserialise(None, bool) is None
    assert unserialise(None, float) is None
    assert unserialise(None, datetime) is None
    assert unserialise(None, date) is None
    assert unserialise(None, time) is None
    assert unserialise(None, List[str]) == []
    assert unserialise(None, Set[str]) == {}


def test_unserialise_list() -> None:
    assert unserialise(["a", "b", "c"], List[str]) == ["a", "b", "c"]
    assert unserialise(["2019-01-20", "2019-02-20", "2019-03-20"], List[date]) == [
        date(year=2019, month=1, day=20),
        date(year=2019, month=2, day=20),
        date(year=2019, month=3, day=20),
    ]


def test_unserialise_set() -> None:
    assert unserialise({"a", "b", "c"}, Set[str]) == {"a", "b", "c"}
    assert unserialise({"2019-01-20", "2019-02-20", "2019-03-20"}, Set[date]) == {
        date(year=2019, month=1, day=20),
        date(year=2019, month=2, day=20),
        date(year=2019, month=3, day=20),
    }
