from typing import List, Optional

from gata import dataclass, field


@dataclass
class Album:
    name: str
    artist: str
    length: float
    songs: List[str]
    tags: Optional[List[str]] = field(default_factory=list)


dict_album = {
    "name": "The Razor's Edge",
    "artist": "AC/DC",
    "length": 64.0,
    "songs": ["Thunderstruck", "Fire Your Guns"],
}

try:
    album = Album(**dict_album)  # validation happens automatically
except ValueError as e:
    ...  # handle error here
