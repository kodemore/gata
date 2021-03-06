# Defining dataclass

Gata provides `gata.dataclass` decorator which can be used as an in-place replacement for `dataclasses.dataclass` decorator.
More about python's dataclasses can be found [here](https://docs.python.org/3/library/dataclasses.html).

```python
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

# file://examples/defining_gata_dataclass.py
```

Additional benefits from using `gata.dataclass` are:

 - easy serialisation with mapping support through `serialise(**mapping)` instance's method
 - validation and deserialisation during class instantiation
 - serialisation through with `dict` function

