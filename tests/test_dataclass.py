from datetime import timedelta
from typing import List

import pytest

from gata.dataclasses import Dataclass, dataclass


def test_define_dataclass() -> None:
    @dataclass()
    class Song:
        album: str
        artist: str
        duration: timedelta

    test_song = Song(album="Test Album", artist="Test Artist", duration=timedelta(days=2))

    assert test_song.artist == "Test Artist"
    assert test_song.album == "Test Album"
    assert test_song.duration == timedelta(days=2)

    test_song.artist = "New Artist"
    assert test_song.artist == "New Artist"

    assert issubclass(Song, Dataclass)
    assert isinstance(test_song, Dataclass)
    assert isinstance(test_song, Song)


def test_frozen_dataclass() -> None:
    @dataclass(frozen=True)
    class Song:
        album: str
        artist: str
        duration: timedelta

    test_song = Song(album="Test Album", artist="Test Artist", duration=timedelta(days=2))

    assert test_song.artist == "Test Artist"

    with pytest.raises(TypeError):
        test_song.artist = "New Artist"


def test_serialise_dataclass() -> None:
    @dataclass()
    class Song:
        album: str
        artist: str
        duration: timedelta

    test_song = Song(album="Test Album", artist="Test Artist", duration=timedelta(days=2))

    assert dict(test_song) == {'album': 'Test Album', 'artist': 'Test Artist', 'duration': 'P2D'}


def test_serialise_nested_dataclasses() -> None:
    @dataclass()
    class Song:
        title: str
        artist: str
        duration: timedelta

    @dataclass()
    class Album:
        title: str
        songs: List[Song]

    song_a = Song(title="Song A", artist="Test Artist", duration=timedelta(minutes=2))
    song_b = Song(title="Song B", artist="Test Artist", duration=timedelta(minutes=3))
    song_c = Song(title="Song C", artist="Test Artist", duration=timedelta(minutes=3, seconds=30))

    test_album: Dataclass = Album(title="Test Album", songs=[song_a, song_b, song_c])

    assert dict(test_album) == {'songs': [{'artist': 'Test Artist', 'duration': 'PT2M', 'title': 'Song A'},
                                          {'artist': 'Test Artist', 'duration': 'PT3M', 'title': 'Song B'},
                                          {'artist': 'Test Artist', 'duration': 'PT3M30S', 'title': 'Song C'}],
                                'title': 'Test Album'}
