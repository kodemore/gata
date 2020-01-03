from .validation_error import ValidationError


class FieldValidationError(ValidationError):
    def __init__(self, field_name: str, previous: ValueError):
        self.field_name = field_name
        self.previous = previous
