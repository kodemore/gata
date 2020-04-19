from dataclasses import dataclass, field
from typing import List, Optional

from gata import validate
from gata.errors import FieldError


@dataclass
class Album:
    name: str
    artist: str
    release_year: int
    tags: Optional[List[str]] = field(default_factory=list)


try:
    album = Album(name="Perfect Strangers", artist="Deep Purple", release_year="1984")
    validate(album)
except FieldError as error:
    print(f"there was an error with validating field: {error.context['field_name']}")
