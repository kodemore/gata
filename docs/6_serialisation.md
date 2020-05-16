# Serialisation

Gata serialisation mechanism is a better alternative to well known `dataclasses.asdict` function.
Differences between `gata`'s serialiser and `asdict` function are:
 - `gata` ensures that returned value matches annotated type
 - `gata` knows how to serialise datetime values, sets, typed lists, typed sets, typed dicts, enums and [more](3_field_types.md)
 - `gata` gives easy interface to implement custom serialisers for your [custom defined types](3_field_types.md#defining-custom-types)


## Serialising gata's dataclasses

You can serialise instance of decorated class simply by using `dict` function on it or directly calling `Class.serialise()` method.

```python
from typing import List

from gata import dataclass


@dataclass(validate=False)
class Album:
    name: str
    artist: str
    release_year: int
    song_list: List[str]


led_zeppelin_I = Album(name="Led Zeppelin I", artist="Led Zeppelin", release_year=1969)

assert led_zeppelin_I.serialise() == {
    "name": "Led Zeppelin I",
    "artist": "Led Zeppelin",
    "release_year": 1969,
    "song_list": [],
}

assert dict(led_zeppelin_I) == led_zeppelin_I.serialise()

# file://examples/serialising_gata_dataclass.py
```

## Serialising python's dataclasses

To serialise instance of python's dataclass use `gata.serialise(obj)` function:

```python
from dataclasses import dataclass
from typing import List

from gata import serialise


@dataclass()
class Album:
    name: str
    artist: str
    release_year: int
    song_list: List[str]


led_zeppelin_I = Album(name="Led Zeppelin I", artist="Led Zeppelin", release_year=1969, song_list=None)

assert serialise(led_zeppelin_I) == {
    "name": "Led Zeppelin I",
    "artist": "Led Zeppelin",
    "release_year": 1969,
    "song_list": [],
}

# file://examples/serialising_python_dataclass.py
```

## Mapping fields

To provide more control over serialisation process you can define custom mapping which will be used during
serialisation process.

```python
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

# file://examples/mapping_fields.py
```

In the above example `Album.name` field was renamed to `album_name` and `song_list` property was excluded from serialisation.

When declaring mapping, mapping field can contain either `str`, `bool` or `dict` value. 
`str` is simply information that its value now is new field's name. `bool` value allows to exclude given field from
serialisation output. `dict` is being used when dealing with nested serialisation.

### Nested mapping

```python
from typing import List

from gata import dataclass
from gata.types import Duration


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

# file://examples/nested_mapping_example.py
```

In the above example we have mapped `Album`'s instance to a dictionary containing:
- `artist_name` which corresponds to `Artist.name` field
- `name` which corresponds to `Album.name` field
- `songs` which corresponds to `Album.song_list` field

Additionally `Song` instances have been transformed to `str` with value corresponding to `Song.title` field. 

> Keep in mind `$item` operator is not required if you are not planning to flatten the structure during serialisation.
