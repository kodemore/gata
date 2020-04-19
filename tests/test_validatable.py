from typing import List, Optional

import pytest

from gata import Field, dataclass
from tests.fixtures import Favourite, PetStatus


def test_validatable() -> None:
    @dataclass()
    class ValidatablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    assert ValidatablePet(name="BoJack", status=PetStatus.AVAILABLE, favourites=[])
    assert hasattr(ValidatablePet, "validate")

    with pytest.raises(ValueError):
        ValidatablePet(name="BoJack", status=10, favourites=[])

    assert ValidatablePet.validate({"name": "BoJack", "status": 0, "favourites": []})


def test_validatable_decorator_without_calling_it() -> None:
    @dataclass()
    class ValidatablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    assert hasattr(ValidatablePet, "validate")


def test_meta_properties_validation() -> None:
    @dataclass
    class ValidatablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

        class Schema:
            favourites = Field(minimum=3)


def test_optional_fields() -> None:
    @dataclass
    class OptionalFieldsTestCase:
        optional_string: Optional[str]
        optional_int: Optional[int]
        optional_float: Optional[float]

    assert OptionalFieldsTestCase.validate({"optional_string": "a"})
    assert OptionalFieldsTestCase.validate({"optional_int": 12})
    assert OptionalFieldsTestCase.validate({"optional_float": 12.1})
