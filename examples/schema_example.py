from typing import List, Optional

from gata import Field, dataclass


@dataclass
class User:
    email: str
    name: str
    age: int = 0
    favourites: Optional[List[str]]

    class Schema:
        email = Field(string_format="email")  # validate email field against email format
        name = Field(minimum=2, maximum=30)  # min name length is 2 characters
        age = Field(minimum=1, maximum=120)  # min user's age is 1 maximum is 120


bob = User(
    email="valid@email.com", name="Bob", age=121
)  # gata.errors.FieldError: Field error `age`: Passed value must be lower than set maximum `120`
