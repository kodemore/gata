from typing import List

from bson import ObjectId

from gata import Field, dataclass


@dataclass()
class Pet:
    id: ObjectId
    tags: List[str]
    name: str = "Boo"
    age: int = 0

    class Schema:
        name = Field(
            minimum=2, maximum=10, serialiser=lambda name: name.strip()
        )  # serialiser set directly in the Field

        # serialiser and deserialiser defined as schema methods
        @staticmethod
        def serialise_id(pet_id: ObjectId) -> str:
            return str(pet_id)

        @staticmethod
        def deserialise_id(pet_id: str) -> ObjectId:
            return ObjectId(pet_id)
