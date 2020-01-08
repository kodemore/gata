from datetime import datetime
import pytest

from gata.errors import FieldError
from tests.fixtures import Favourite
from tests.fixtures import Pet


def test_validate_data_with_dataclass() -> None:
    try:
        Pet.validate({"age": 120})
    except FieldError as error:
        assert error.field_name == "age"


def test_unserialise_dataclass() -> None:
    pet = Pet.unserialise(
        {
            "name": "Tom",
            "age": 10,
            "favourites": [{"name": "bones"}, {"name": "sousage"}],
            "status": 1,
            "created_at": "2020-01-01 10:10:10",
        }
    )

    assert isinstance(pet, Pet)
    assert isinstance(pet.favourites[0], Favourite)
    assert isinstance(pet.created_at, datetime)


def test_serialise_dataclass() -> None:
    pet = Pet("Boo", 20)
    assert pet.serialise() == {
        "name": "Boo",
        "age": 20,
        "favourites": [],
        "tags": [],
        "status": 0,
        "created_at": None,
    }


def test_unserialise_dataclass_with_invalid_fields() -> None:
    with pytest.raises(AttributeError):
        Pet.unserialise({"pet_name": "Tom"})


def test_validate_with_unknown_field() -> None:
    with pytest.raises(ValueError):
        Pet.validate(
            {
                "pet_name": "Tom",
                "age": 20,
                "favourites": [],
                "tags": [],
                "status": 0,
                "created_at": None,
            }
        )


def test_validate_success() -> None:
    assert Pet.validate(
        {
            "name": "Tom",
            "age": 20,
            "favourites": [],
            "tags": [],
            "status": 0,
            "created_at": "2019-01-01T10:10:10",
        }
    )


def test_set_unkown_attribute() -> None:
    pet = Pet()
    with pytest.raises(AttributeError):
        pet.fail = 2


def test_get_unkown_attribute() -> None:
    pet = Pet()
    with pytest.raises(AttributeError):
        fail = pet.fail
