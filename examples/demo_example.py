from datetime import datetime
from typing import List, Optional

from gata import dataclass


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0
    sold_at: Optional[datetime] = None


try:
    pet = Pet()
except ValueError:
    pass  # tags are required and undefined, so error will be thrown


pet = Pet(**{"tags": ["dog"]})

assert pet.serialise() == {'tags': ['dog'], 'name': 'Boo', 'age': 0, 'sold_at': None}
assert pet.serialise(age=False, sold_at=False) == {'tags': ['dog'], 'name': 'Boo'}
