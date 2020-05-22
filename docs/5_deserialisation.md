# Deserialisation

## Automatic deserialisation

When dataclass is decorated with `gata.dataclass` decorator like below, deserialisation happens automatically.

```python
from typing import List

from gata import dataclass


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

# file://examples/automatic_deserialisation.py
```

> Additional fields that exists in the dictionary which have no corresponding fields declared in dataclass are simply ignored.

## Manual deserialisation

To deserialise dict into dataclass simply use `gata.deserialise(dict, classname)` function like below:

```python
from dataclasses import dataclass
from typing import List

from gata import deserialise


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

led_zeppelin_I = deserialise(raw_album, Album)

assert isinstance(led_zeppelin_I, Album)
assert len(led_zeppelin_I.song_list) == 9
assert led_zeppelin_I.song_list[3] == "Thank You"

# file://examples/manual_deserialisation.py
```

> Additional fields that exists in the dictionary which have no corresponding fields declared in dataclass are simply ignored.


## Nested deserialisation
The following example shows how simply you can deserialise very complex objects.

```python
from datetime import timedelta
from typing import List

from gata import dataclass
from gata.mapping import TimedeltaMapping


@dataclass
class Artist:
    name: str


@dataclass
class Song:
    title: str
    length: TimedeltaMapping


@dataclass
class Album:
    name: str
    artist: Artist
    release_year: int
    song_list: List[Song]


raw_album = {
    "name": "Led Zeppelin I",
    "artist": {"name": "Led Zeppelin"},
    "release_year": 1969,
    "some_unknown_field": False,
    "song_list": [
        {"title": "Whole Lotta Love", "length": "PT5M34S",},
        {"title": "What Is and What Should Never Be", "length": "PT4M46S",},
    ],
}

led_zeppelin_I = Album(**raw_album)

assert isinstance(led_zeppelin_I, Album)
assert isinstance(led_zeppelin_I.artist, Artist)
for song in led_zeppelin_I.song_list:
    assert isinstance(song, Song)
    assert isinstance(song.length, timedelta)

# file://examples/nested_deserialisation.py
```

> Keep in mind during deserialisation validation still happens behind the scenes 
> if nested data requires deserialisation.
