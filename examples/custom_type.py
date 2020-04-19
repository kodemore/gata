import re
from typing import Any

from gata import dataclass
from gata.errors import ValidationError
from gata.typing import SerialisableType, ValidatableType

UK_POST_CODE_REGEX = re.compile(
    "^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([AZa-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$"
)


class UKPostCode(str, SerialisableType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        if UK_POST_CODE_REGEX.match(value):
            return value
        raise ValidationError(f"passed value {value} is not valid uk post code")

    @classmethod
    def serialise(cls, value: Any) -> Any:
        return value

    @classmethod
    def deserialise(cls, value: Any) -> Any:
        return value


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
