from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from typing_extensions import TypedDict

from gata.schema import Field


class PetStatus(Enum):
    AVAILABLE = 0
    SOLD = 1
    RESERVED = 2


@dataclass
class Favourite:
    name: str
    priority: int = 0


class PetDict(TypedDict):
    tags: List[str]
    name: str
    age: int


@dataclass()
class Pet:
    """
    Some pet description
    """

    name: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    favourites: List[Favourite] = field(default_factory=list)
    status: PetStatus = PetStatus.AVAILABLE
    age: int = 0

    class Schema:
        tags = Field(minimum=1)
        name = Field(minimum=2, maximum=20)
        age = Field(minimum=0, maximum=100)


@dataclass
class PetWithVirtualProperties:
    name: str
    favourite: Favourite
    favourite_id: int = field(default=None)

    class Schema:
        favourite_id = Field(write_only=True)
        favourite = Field(read_only=True)
