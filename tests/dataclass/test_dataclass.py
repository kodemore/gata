from dataclasses import field
from datetime import date
from typing import Optional

import pytest

from gata import Field, dataclass, validate, deserialise, serialise


def test_args_in_dataclass() -> None:
    @dataclass
    class Audio:
        title: str
        length: float
        artist: str

    def assert_instance(obj: Audio) -> None:
        assert obj.title == "My Audio I"
        assert obj.length == 10.12
        assert obj.artist == "Me"

    assert_instance(Audio("My Audio I", 10.12, "Me"))
    assert_instance(Audio("My Audio I", 10.12, artist="Me"))
    assert_instance(Audio("My Audio I", length=10.12, artist="Me"))
    assert_instance(Audio(title="My Audio I", length=10.12, artist="Me"))


def test_frozen_dataclass() -> None:
    @dataclass(frozen=True)
    class FrozenAudio:
        name: str
        length: float
        artist: str

    audio = FrozenAudio(name="My Audio 1", length=1.12, artist="Me")

    with pytest.raises(TypeError):
        audio.name = "New name"

    with pytest.raises(TypeError):
        audio.non_existing_field = "New value"

    assert audio.name == "My Audio 1"


def test_repr_dataclass() -> None:
    @dataclass
    class Audio:
        name: str
        length: float
        artist: str

    test_instance = Audio(name="Audio 1", length=10.0, artist="Me")

    assert repr(test_instance) == f"{Audio.__qualname__}(name='Audio 1', length=10.0, artist='Me')"


def test_nested_repr_dataclass() -> None:
    @dataclass
    class Artist:
        name: str

    @dataclass(frozen=True)
    class FrozenAudio:
        name: str
        length: float = field(repr=False)
        artist: Artist

    test_instance = FrozenAudio(name="Audio 1", length=10.0, artist=Artist(name="Me"))
    assert repr(test_instance) == f"{FrozenAudio.__qualname__}(name='Audio 1', artist={Artist.__qualname__}(name='Me'))"


def test_eq_dataclass() -> None:
    @dataclass
    class Artist:
        name: str
        age: int
        albums: Optional[int] = Field(compare=False, default=0)

    @dataclass
    class OtherArtist:
        name: str
        age: int

    assert Artist(name="Bob", age=15, albums=2) == Artist(name="Bob", age=15, albums=1)
    assert Artist(name="Bob", age=15) != Artist(name="Bob", age=16)
    assert OtherArtist(name="Bob", age=15) != Artist(name="Bob", age=15)


def test_notimplemented() -> None:
    with pytest.raises(NotImplementedError):

        @dataclass(unsafe_hash=True)
        class TestNotImplemented:
            pass


def test_fail_frozen_on_dataclass_without_init() -> None:
    with pytest.raises(ValueError):

        @dataclass(init=False, frozen=True)
        class TestNotImplemented:
            pass


def test_deserialise_and_serialise_dataclass() -> None:
    @dataclass
    class Artist:
        name: str

    @dataclass
    class Song:
        title: str = Field(minimum=2, maximum=120)
        artist: Artist
        length: int
        release_date: date

    raw_song = {
        "title": "Take Five",
        "artist": {"name": "The Dave Brubeck Quartet"},
        "length": 324,
        "release_date": "1959-06-01",
    }

    take_five = deserialise(raw_song, Song)

    assert isinstance(take_five, Song)
    assert isinstance(take_five.artist, Artist)

    assert serialise(take_five) == raw_song
    assert dict(take_five) == serialise(take_five)


def test_fail_validate_dataclass() -> None:
    with pytest.raises(ValueError):
        assert validate(1)


def test_fail_serialise_non_dataclass() -> None:
    class Artist:
        pass

    with pytest.raises(ValueError):
        serialise(Artist())


def test_fail_deserialise_non_dataclass() -> None:
    class Artist:
        pass

    with pytest.raises(ValueError):
        deserialise(1, Artist)
