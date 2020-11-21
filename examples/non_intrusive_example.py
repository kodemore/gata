from typing import List
from gata import validate_dataclass, asdict
from dataclasses import dataclass


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0


try:
    pet = Pet(tags="a")
    validate_dataclass(pet)
except ValueError as error:
    pass  # tags are required and undefined, so error will be thrown


pet = Pet(**{"tags": ["dog"]})

assert asdict(pet) == {"tags": ["dog"], "name": "Boo", "age": 0}  # serialise object

# exclude `age` field from serialisation, and rename `name` field to `pet_name`
assert asdict(pet, {"age": False, "name": "pet_name"}) == {
    "tags": ["dog"],
    "pet_name": "Boo",
}

print(pet)
