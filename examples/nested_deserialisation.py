from datetime import timedelta
from typing import List

from gata import dataclass
from gata.typing import Duration


@dataclass
class Artist:
    name: str


@dataclass
class Song:
    title: str
    length: Duration


@dataclass
class Album:
    name: str
    artist: Artist
    release_year: int
    song_list: List[Song]


raw_album = {
    "name": "Led Zeppelin I",
    "artist": {
        "name": "Led Zeppelin"
    },
    "release_year": 1969,
    "some_unknown_field": False,
    "song_list": [
        {
            "title": "Whole Lotta Love",
            "length": "PT5M34S",
        },
        {
            "title": "What Is and What Should Never Be",
            "length": "PT4M46S",
        },
    ]
}

led_zeppelin_I = Album(**raw_album)

assert isinstance(led_zeppelin_I, Album)
assert isinstance(led_zeppelin_I.artist, Artist)
for song in led_zeppelin_I.song_list:
    assert isinstance(song, Song)
    assert isinstance(song.length, timedelta)
