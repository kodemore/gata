from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from gata.types.utils import map_type
import typing

import pytest

from gata import types


@pytest.mark.parametrize(
    "base_type, expected_type",
    [
        (int, types.Integer),
        (bool, types.Boolean),
        (float, types.Number),
        (str, types.String),
        (list, types.Array),
        (tuple, types.Array),
    ],
)
def test_map_base_types(base_type, expected_type) -> None:
    assert map_type(base_type) == expected_type


def test_map_datetime() -> None:
    translated_type = map_type(datetime)
    assert isinstance(translated_type, types.String.__class__)
    assert translated_type.format == types.string.Format.DATETIME


def test_map_date() -> None:
    translated_type = map_type(date)
    assert isinstance(translated_type, types.String.__class__)
    assert translated_type.format == types.string.Format.DATE


def test_map_time() -> None:
    translated_type = map_type(time)
    assert isinstance(translated_type, types.String.__class__)
    assert translated_type.format == types.string.Format.TIME


def test_map_set() -> None:
    translated_type = map_type(set)
    assert translated_type.unique_items
    assert isinstance(translated_type, types.Array.__class__)

    translated_type = map_type(typing.Set)
    assert isinstance(translated_type, types.Array.__class__)
    assert translated_type.unique_items


def test_map_enum() -> None:
    class TestEnum(Enum):
        ITEM_1 = 1
        ITEM_2 = "two"

    translated_type: types.Enum.__class__ = map_type(TestEnum)

    assert isinstance(translated_type, types.Enum.__class__)
    assert translated_type.values == {1, "two"}
    assert translated_type.target == TestEnum


@pytest.mark.parametrize(
    "typing_type, expected_type",
    [
        (typing.List, types.Array),
        (typing.Sequence, types.Array),
        (typing.Iterable, types.Array),
        (typing.Tuple, types.Array),
    ],
)
def test_map_typing_type(typing_type, expected_type) -> None:
    assert map_type(typing_type) == expected_type


def test_map_complex_list() -> None:
    mapped_type: types.Array.__class__ = map_type(typing.List[str])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.String

    mapped_type: types.Array.__class__ = map_type(typing.List[typing.List[datetime]])
    assert isinstance(mapped_type, types.Array.__class__)
    assert isinstance(mapped_type.items, types.Array.__class__)
    assert mapped_type.items.items, types.DateTime

    mapped_type: types.Array.__class__ = map_type(typing.List[typing.Any])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.Any


def test_map_complex_sequence() -> None:
    mapped_type: types.Array.__class__ = map_type(typing.Sequence[str])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.String

    mapped_type: types.Array.__class__ = map_type(typing.Sequence[typing.Any])
    assert isinstance(mapped_type, types.Array.__class__)
    assert mapped_type.items == types.Any


def test_map_optional_types() -> None:
    mapped_type: types.Integer.__class__ = map_type(typing.Optional[int])
    assert isinstance(mapped_type, types.Integer.__class__)
    assert mapped_type.nullable


def test_map_union_type() -> None:
    mapped_type: types.AnyOf.__class__ = map_type(typing.Union[str, int])
    assert isinstance(mapped_type, types.AnyOf.__class__)
    assert isinstance(mapped_type.types[0], types.String.__class__)
    assert isinstance(mapped_type.types[1], types.Integer.__class__)

    mapped_type: types.AnyOf.__class__ = map_type(
        typing.Union[typing.Optional[str], typing.Optional[int], None]
    )


@pytest.mark.parametrize("input", [types.Any, types.Enum])
def test_map_gata_types(input) -> None:
    assert input == map_type(input)
