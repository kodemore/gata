from datetime import timedelta
from typing import List, Optional

import pytest

from gata.dataclasses import Dataclass, dataclass, field


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


def test_serialise_with_mapping() -> None:
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

    test_album: Dataclass = Album(title="Test Album", songs=[song_a])

    assert test_album.serialise(title="album_title", songs={"$item": "title"}) == {'album_title': 'Test Album', 'songs': ['Song A']}


def test_deserialise_into_dataclass() -> None:
    @dataclass()
    class Song:
        title: str
        artist: str
        duration: timedelta

    @dataclass()
    class Album:
        title: str
        songs: List[Song]

    raw_data = {
        "title": "Test Album",
        "songs": [
            {
                "title": "Song A",
                "artist": "Test artist",
                "duration": "PT3M20S",
            },
            {
                "title": "Song B",
                "artist": "Test artist",
                "duration": "PT4M",
            },
        ]
    }

    album = Album(**raw_data)

    assert isinstance(album, Album)
    for song in album.songs:
        assert isinstance(song, Song)
        assert isinstance(song.duration, timedelta)
        assert song.artist == "Test artist"


def test_validate_dataclass() -> None:

    @dataclass()
    class Song(Dataclass):
        album: str
        artist: Optional[str]
        duration: timedelta

    assert Song.validate({
        "album": "Test Album",
        "duration": "PT3M"
    }) is None

    with pytest.raises(ValueError):
        assert Song.validate({
            "album": "Test Album",
            "artist": "Test Artist",
            "duration": "3 minutes",
        }) is None


def test_deserialise_without_validation_into_dataclass() -> None:
    @dataclass(validate=False)
    class Song:
        title: str
        artist: str
        duration: timedelta

    @dataclass(validate=False)
    class Album:
        title: str
        songs: List[Song]

    raw_data = {
        "title": "Test Album",
        "songs": [
            {
                "title": "Song A",
                "artist": "Test artist",
                "duration": "PT3M20S",
            },
            {
                "title": "Song B",
                "artist": "Test artist",
                "duration": "PT4M",
            },
        ]
    }

    album = Album(**raw_data)

    assert isinstance(album, Album)
    for song in album.songs:
        assert isinstance(song, Song)
        assert isinstance(song.duration, timedelta)
        assert song.artist == "Test artist"


def test_deserialise_read_only_properties() -> None:
    @dataclass(validate=False)
    class Song:
        title: str
        artist: str = field(read_only=True)
        duration: timedelta

    @dataclass(validate=False)
    class Album:
        title: str
        songs: List[Song]

    raw_data = {
        "title": "Test Album",
        "songs": [
            {
                "title": "Song A",
                "artist": "Test artist",
                "duration": "PT3M20S",
            },
            {
                "title": "Song B",
                "artist": "Test artist",
                "duration": "PT4M",
            },
        ]
    }

    album = Album(**raw_data)

    assert isinstance(album, Album)
    for song in album.songs:
        assert isinstance(song, Song)
        assert isinstance(song.duration, timedelta)
        assert song.artist is None


def test_deserialise_with_defaults() -> None:
    @dataclass
    class Song:
        title: str = "Default Title"
        artist: str = "Default Artist"
        duration: timedelta

    raw_data = {
        "duration": "PT3M"
    }

    song = Song(**raw_data)

    assert isinstance(song, Song)
    assert isinstance(song.duration, timedelta)
    assert song.title == "Default Title"
    assert song.artist == "Default Artist"


def test_dataclass_eq() -> None:
    @dataclass
    class Song:
        title: str = "Default Title"
        artist: str = "Default Artist"
        duration: timedelta

    raw_data = {
        "duration": "PT3M"
    }

    song_1 = Song(**raw_data)
    song_2 = Song(**raw_data)
    song_3 = Song(**{"title": "Sample Title", "duration": "PT3M"})

    assert song_1 == song_2
    assert song_1 != song_3


def test_initialise_dataclass_with_pos_arguments() -> None:
    @dataclass
    class Song:
        title: str = "Default Title"
        artist: str = "Default Artist"
        duration: timedelta

    song = Song("Title", "Artist", "PT3M")

    assert song.title == "Title"
    assert song.artist == "Artist"
    assert song.duration == timedelta(minutes=3)
