from typing import List
from gata import dataclass


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0


try:
    pet = Pet()
except ValueError as error:  # gata.errors.FieldError
    pass  # tags are required and undefined, so error will be thrown


pet = Pet(**{"tags": ["dog"]})

assert pet.serialise() == {"tags": ["dog"], "name": "Boo", "age": 0}  # serialise object

# exclude `age` field from serialisation, and rename `name` field to `pet_name`
assert pet.serialise(age=False, name="pet_name") == {"tags": ["dog"], "pet_name": "Boo"}
