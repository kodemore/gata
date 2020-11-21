from typing import List, Optional

from gata import dataclass, field


@dataclass
class User:
    email: str = field(
        string_format="email"
    )  # validate email field against email format
    name: str = field(minimum=2, maximum=30)  # min name length is 2 characters
    age: int = field(
        minimum=1, maximum=120, default=0
    )  # min user's age is 1 maximum is 120
    favourites: Optional[List[str]]


bob = User(
    email="valid@email.com", name="Bob", age=121
)  # gata.errors.MaximumBoundError: Field error `age`: Passed value must be lower than set maximum `120`
