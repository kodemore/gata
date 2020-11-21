from dataclasses import dataclass
from typing import List
from gata import asdict


@dataclass()
class Album:
    name: str
    artist: str
    release_year: int
    song_list: List[str]


led_zeppelin_I = Album(
    name="Led Zeppelin I", artist="Led Zeppelin", release_year=1969, song_list=None
)

assert asdict(led_zeppelin_I) == {
    "name": "Led Zeppelin I",
    "artist": "Led Zeppelin",
    "release_year": 1969,
    "song_list": [],
}
