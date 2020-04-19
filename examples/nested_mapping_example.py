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


song_1 = Song(title="Whole lotta rosie", length="PT5M40S")
song_2 = Song(title="Thunderstruck", length="PT4M38S")
artist = Artist(name="AC/DC")
album = Album(name="Best of AC/DC", artist=artist, release_year=1989, song_list=[song_1, song_2])

serialised_album = album.serialise(
    artist={
        "$self": "artist_name",  # artist field now becomes `artist_name`
        "$item": "name",  # and artist will be returned as a string containing Artist.name's value
    },
    release_year=False,
    song_list={
        "$self": "songs",  # song_list field will be mapped to `songs`
        "$item": "title",  # and each song now becomes now just a string with its `title`
    }
)

assert serialised_album == {
    "name": "Best of AC/DC",
    "artist_name": "AC/DC",
    "songs": [
        "Whole lotta rosie",
        "Thunderstruck",
    ]
}
