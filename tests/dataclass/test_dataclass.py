from dataclasses import field

import pytest

from gata import dataclass


def test_frozen_dataclass() -> None:
    @dataclass(frozen=True)
    class FrozenAudio:
        name: str
        length: float
        artist: str

    audio = FrozenAudio(name="My Audio 1", length=1.12, artist="Me")

    with pytest.raises(TypeError):
        audio.name = "New name"

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
