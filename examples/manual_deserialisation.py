from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    name: str
    artist: str
    release_year: int
    song_list: List[str]


raw_album = {
    "name": "Led Zeppelin I",
    "artist": "Led Zeppelin",
    "release_year": 1969,
    "some_unknown_field": False,
    "song_list": [
        "Whole Lotta Love",
        "What Is and What Should Never Be",
        "The Lemon Song",
        "Thank You",
        "Heartbreaker",
        "Living Loving Maid",
        "Ramble On",
        "Moby Dick",
        "Bring It On Home",
    ],
}

led_zeppelin_I = Album(**raw_album)

assert isinstance(led_zeppelin_I, Album)
assert len(led_zeppelin_I.song_list) == 9
assert led_zeppelin_I.song_list[3] == "Thank You"
