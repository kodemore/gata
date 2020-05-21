import re
from typing import Any

from gata import dataclass, Type
from gata.errors import ValidationError

UK_POST_CODE_REGEX = re.compile(
    "^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([AZa-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$"
)


class UKPostCode(Type):
    def __init__(self, value: Any):
        self.value = str(value)

    def validate(self) -> Any:
        if UK_POST_CODE_REGEX.match(self.value):
            return self.value
        raise ValidationError(f"passed value {self.value} is not valid uk post code")

    def serialise(self) -> Any:
        return self.value


@dataclass
class User:
    name: str
    post_code: UKPostCode
    age: int


bob = User(name="Bob", post_code="SW16 5QW", age=22)

try:
    failed_tom = User(name="Tom", post_code="123111", age=28)
except ValidationError as error:
    ...
