from gata.utils import is_dataclass_like, is_gataclass, is_typed_dict, is_optional_type
from dataclasses import dataclass
from gata.dataclasses import dataclass as gataclass
from typing_extensions import TypedDict
from typing import Optional, List, Union
import pytest


def test_is_dataclass_like() -> None:
    @dataclass()
    class Dataclass:
        field_a: str

    class DataclassLike:
        field_a: str
        field_b: int

    class NotDataclassLike:
        pass

    assert is_dataclass_like(DataclassLike)
    assert is_dataclass_like(Dataclass)
    assert is_dataclass_like(Dataclass(field_a="a"))
    assert is_dataclass_like(DataclassLike())
    assert not is_dataclass_like(NotDataclassLike)


def test_is_gataclass() -> None:
    @gataclass
    class Dataclass:
        field_a: str

    class DataclassLike:
        field_a: str
        field_b: int

    assert is_gataclass(Dataclass)
    assert not is_gataclass(DataclassLike)


def test_is_typed_dict() -> None:
    Song = TypedDict("Song", {"title": str, "artist": str})

    class ClassSong(TypedDict):
        title: str
        artist: str

    class NotTypedDict:
        pass

    @dataclass()
    class Dataclass:
        pass

    assert is_typed_dict(Song)
    assert is_typed_dict(ClassSong)
    assert not is_typed_dict(NotTypedDict)
    assert not is_typed_dict(Dataclass)
    assert not is_typed_dict(str)


def test_is_optional_type() -> None:
    assert is_optional_type(Optional[int])
    assert is_optional_type(Optional[List])
    assert is_optional_type(Union[None, List])
    assert not is_optional_type(int)
    assert not is_optional_type(str)
    assert not is_optional_type(List)
