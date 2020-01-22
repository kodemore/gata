from typing import Any


class ValidationError(ValueError):
    code: str
    message: str

    def __init__(self, *args, **kwargs: Any):
        if "code" in kwargs:
            self.code = kwargs["code"]

        self.context = kwargs
        if args:
            super().__init__(*args)
        else:
            super().__init__(str(self))

    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return self.message.format(**self.context)


class TypeValidationError(ValidationError):
    code = "type_error"
    message = "Passed value must be valid {expected_type} type."


class FormatValidationError(ValidationError):
    code = "format_error"
    message = "Passed value must be valid string format: {expected_format}."


class IterableValidationError(TypeValidationError):
    code = "iterable_error"
    message = "Passed value is not expected iterable type."


class UniqueValidationError(TypeValidationError):
    code = "unique_error"
    message = "Passed value must contain only unique items."


class ArithmeticValidationError(ValidationError, ArithmeticError):
    code = "arithmetic_error"
    message = "Passed value is invalid."


class LengthValidationError(ArithmeticValidationError):
    pass


class BoundValidationError(ArithmeticValidationError):
    pass


class MinimumBoundError(BoundValidationError):
    code = "minimum_bound"
    message = "Passed value must be greater than set minimum `{expected_minimum}`."


class MaximumBoundError(BoundValidationError):
    code = "maximum_bound"
    message = "Passed value must be lower than set maximum `{expected_maximum}`."


class MinimumLengthError(LengthValidationError):
    code = "minimum_length"
    message = (
        "Passed value's length must be greater than set minimum `{expected_minimum}`."
    )


class MaximumLengthError(LengthValidationError):
    code = "maximum_length"
    message = (
        "Passed value's length must be lower than set maximum `{expected_maximum}`."
    )


class FieldError(ValidationError):
    code = "field_error"
    message = "Field error `{field_name}`: "

    def __init__(self, field: str, caused_by: ValidationError):
        self.context = {"field_name": field, **caused_by.context}
        self.caused_by = caused_by

    def __str__(self) -> str:
        return self.message.format(**self.context) + str(self.caused_by)


class TypeMapError(RuntimeError):
    pass


class SerialisationError(ValueError, TypeMapError):
    pass


class DeserialisationError(ValueError, TypeMapError):
    pass
