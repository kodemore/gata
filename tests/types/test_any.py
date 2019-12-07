from gata.types import *


def test_validate_any() -> None:
    validator = Any
    validator.validate(None)
