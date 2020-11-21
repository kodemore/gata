from typing import List

from gata import dataclass


@dataclass
class Album:
    name: str
    artist: str
    songs: List[str]

    def __post_init__(self) -> None:
        self.songs_count = len(self.songs)


dict_album = {
    "name": "The Razor's Edge",
    "artist": "AC/DC",
    "songs": ["Thunderstruck", "Fire Your Guns"],
}

album = Album(**dict_album)
print(album.songs_count)  # will print 2
