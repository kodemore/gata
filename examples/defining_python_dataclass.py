from dataclasses import dataclass, field
from typing import List, Optional

import gata


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
    gata.validate(dict_album, Album)
    album = Album(**dict_album)
except ValueError as e:
    ...  # handle error here
