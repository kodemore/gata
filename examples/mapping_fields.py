from typing import List

from gata import dataclass


@dataclass(validate=False)  # Turn off validation during instantiation
class Album:
    name: str
    artist: str
    release_year: int
    song_list: List[str]


led_zeppelin_I = Album(name="Led Zeppelin I", artist="Led Zeppelin", release_year=1969)

serialised = led_zeppelin_I.serialise(
    name="album_name",  # rename `name` field to `album_name`
    song_list=False,  # ignore song_list field during serialisation
)

assert serialised == {
    "album_name": "Led Zeppelin I",
    "artist": "Led Zeppelin",
    "release_year": 1969,
}
