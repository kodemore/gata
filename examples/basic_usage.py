from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0
    sold_at: Optional[datetime] = None
