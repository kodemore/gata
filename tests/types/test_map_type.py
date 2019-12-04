from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
import typing

import pytest

from gata import types


@pytest.mark.parametrize("base_type, expected_type", [
    (int, types.Integer),
    (bool, types.Boolean),
    (float, types.Number),
    (str, types.String),
    (list, types.Array),
    (tuple, types.Array),
])
def test_map_base_types(base_type, expected_type) -> None:
    assert types.map_type(base_type) == expected_type


def test_map_set() -> None:
    translated_type = types.map_type(set)
    assert translated_type.unique_items
    assert isinstance(translated_type, types.Array.__class__)

    translated_type = types.map_type(typing.Set)
    assert isinstance(translated_type, types.Array.__class__)
    assert translated_type.unique_items


def test_map_enum() -> None:
    class TestEnum(Enum):
        ITEM_1 = 1
        ITEM_2 = "two"

    translated_type: types.Enum.__class__ = types.map_type(TestEnum)

    assert isinstance(translated_type, types.Enum)
    assert translated_type.values == (1, "two")


@pytest.mark.parametrize("typing_type, expected_type", [
    (datetime, types.DateTime),
    (date, types.Date),
    (time, types.Time),
    (typing.List, types.Array),
    (typing.Sequence, types.Array),
    (typing.Iterable, types.Array),
    (typing.Tuple, types.Array),
])
def test_map_typing_type(typing_type, expected_type) -> None:
    assert types.map_type(typing_type) == expected_type


def test_complex_list() -> None:
    mapped_type: types.Array.__class__ = types.map_type(typing.List[str])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.String

    mapped_type: types.Array.__class__ = types.map_type(typing.List[typing.List[datetime]])
    assert isinstance(mapped_type, types.Array.__class__)
    assert isinstance(mapped_type.items, types.Array.__class__)
    assert mapped_type.items.items, types.DateTime

    mapped_type: types.Array.__class__ = types.map_type(typing.List[typing.Any])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.Any


def test_complex_sequence() -> None:
    mapped_type: types.Array.__class__ = types.map_type(typing.Sequence[str])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.String

