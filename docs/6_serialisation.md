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
