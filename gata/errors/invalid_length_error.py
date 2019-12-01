from .validation_error import ValidationError


class InvalidLengthError(ValidationError):
    pass


class OverflowError(InvalidLengthError):
    pass


class UnderflowError(InvalidLengthError):
    pass


__all__ = ["InvalidLengthError", "OverflowError", "UnderflowError"]
