import numbers
from typing import Any
from typing import Optional

from gata.errors import ValidationError
from gata.validators import validate_multiple_of
from gata.validators import validate_range
from .type import Type


class NumberType(Type):
    def __init__(self):
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.multiple_of = None

    def validate(self, value: Any):
        if value is None and self.nullable:
            return None

        if isinstance(value, bool) or not isinstance(
            value, (int, float, complex, numbers.Number, numbers.Real, numbers.Rational)
        ):
            raise ValidationError("Passed value is not a valid integer number.")

        if self.minimum is not None or self.maximum is not None:
            validate_range(value, self.minimum, self.maximum)  # type: ignore

        if self.multiple_of is not None:
            validate_multiple_of(value, self.multiple_of)  # type: ignore

    def __call__(
        self,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        multiple_of: Optional[float] = None,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> "NumberType":
        instance: NumberType = super().__call__(
            deprecated, write_only, read_only, nullable, default
        )
        instance.minimum = minimum
        instance.maximum = maximum
        instance.multiple_of = multiple_of

        return instance


Number = NumberType()


__all__ = ["Number"]
