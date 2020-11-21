from typing import List

from gata import dataclass


@dataclass(validate=False)
class Album:
    name: str
    artist: str
    release_year: int
    song_list: List[str]


led_zeppelin_I = Album(name="Led Zeppelin I", artist="Led Zeppelin", release_year=1969)

led_zeppelin_I.serialise()
