from typing import List
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing_extensions import TypedDict


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

    class Meta:
        tags = {"min": 1}
        name = {"min": 2, "max": 20}
        age = {"min": 0, "max": 100}
