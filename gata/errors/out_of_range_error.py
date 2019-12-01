from .validation_error import ValidationError


class OutOfRangeError(ValidationError):
    pass


class NotWithinMinimumBoundaryError(OutOfRangeError):
    pass


class NotWithinMaximumBoundaryError(OutOfRangeError):
    pass


__all__ = [
    "OutOfRangeError",
    "NotWithinMinimumBoundaryError",
    "NotWithinMaximumBoundaryError",
]
