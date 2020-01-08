from gata import DataClass
from typing import List
from datetime import datetime
from enum import Enum


class PetStatus(Enum):
    AVAILABLE = 0
    SOLD = 1
    RESERVED = 2


class Favourite(DataClass):
    name: str
    priority: int = 0

    def __init__(self, name: str, priority: int = 0):
        self.name = name
        self.priority = priority


class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    favourites: List[Favourite]
    tags: List[str]
    status: PetStatus = PetStatus.AVAILABLE
    created_at: datetime

    class Meta:
        tags = {"items": {"min": 2, "max": 10}}
        name = {"min": 2, "max": 20}
        age = {"min": 0, "max": 100}

    def __init__(self, name: str = "Pimpek", age: int = 0):
        self.name = name
        self.favourites = []
        self.tags = []
        self.age = age
