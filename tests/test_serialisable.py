from dataclasses import dataclass
from typing import List

from gata import serialisable
from tests.fixtures import Favourite, PetStatus


def test_serialisable_decorator():
    @serialisable()
    @dataclass()
    class SerialisablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    pet = SerialisablePet(name="Tom", status=PetStatus.AVAILABLE, favourites=[Favourite("bone")])

    assert hasattr(pet, "serialise")
    assert pet.serialise() == {
        "favourites": [{"name": "bone", "priority": 0}],
        "name": "Tom",
        "status": 0,
    }

    assert hasattr(SerialisablePet, "deserialise")
    deserialised_tom = SerialisablePet.deserialise(
        {"favourites": [{"name": "bone", "priority": 0}], "name": "Tom", "status": 0}
    )

    assert isinstance(deserialised_tom, SerialisablePet)
    assert isinstance(deserialised_tom.favourites[0], Favourite)
    assert deserialised_tom.name == "Tom"
    assert deserialised_tom.status is PetStatus.AVAILABLE


def test_decorator_without_calling_it() -> None:
    @serialisable
    @dataclass()
    class SerialisablePet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    pet = SerialisablePet(name="Tom", status=PetStatus.AVAILABLE, favourites=[Favourite("bone")])
    assert pet.serialise() == {
        "favourites": [{"name": "bone", "priority": 0}],
        "name": "Tom",
        "status": 0,
    }


def test_serialisable_with_mapping() -> None:
    @serialisable
    @dataclass
    class Pet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

    @serialisable
    @dataclass
    class PetStore:
        name: str
        pets: List[Pet]

    tom = Pet(name="Tom", status=PetStatus.AVAILABLE, favourites=[Favourite("bone")])
    bob = Pet(name="Bob", status=PetStatus.RESERVED, favourites=[Favourite("candy")])

    store = PetStore(name="happy pets", pets=[tom, bob])

    def map_favourites(favorites: List[Favourite]) -> (str, list):
        return "favourite_list", [{"name": favorites[0].name}]

    assert hasattr(store, "serialise")
    assert store.serialise(pets={"$self": "pet_list", "favourites": map_favourites, "status": "pet_status"}) == {
        "name": "happy pets",
        "pet_list": [
            {"name": "Tom", "favourite_list": [{"name": "bone"}], "pet_status": 0},
            {"name": "Bob", "favourite_list": [{"name": "candy"}], "pet_status": 2},
        ],
    }


def test_serialisable_with_custom_serialisers_deserialisers() -> None:
    @serialisable
    @dataclass
    class Pet:
        name: str
        status: PetStatus
        favourites: List[Favourite]

        class Meta:
            @staticmethod
            def serialise_name(name: str) -> str:
                return f"serialised: {name}"

            @staticmethod
            def deserialise_favourites(favourites: List[str]) -> List[Favourite]:
                return [Favourite(name=favourite) for favourite in favourites if favourite]

    @serialisable
    @dataclass
    class PetStore:
        name: str
        pets: List[Pet]

    pet_store = PetStore.deserialise(
        {
            "name": "Happy Pets",
            "pets": [{"name": "Boo", "favourites": ["bone", "candy"]}, {"name": "Koo", "favourites": ["seeds"]},],
        }
    )

    assert isinstance(pet_store, PetStore)
    assert pet_store.name == "Happy Pets"
    for pet in pet_store.pets:
        assert isinstance(pet, Pet)
        for favourite in pet.favourites:
            assert isinstance(favourite, Favourite)


def test_serialise_non_data_class() -> None:
    @serialisable
    class Pet:
        name: str
        status: PetStatus
        favourites: List[str]

        def __init__(self, name: str, status: PetStatus, favourites: List[str] = []):
            self.name = name
            self.status = status
            self.favourites = favourites

    pet = Pet("Boo", PetStatus.AVAILABLE, ["bone", "candy"])

    assert pet.serialise() == {
        "name": "Boo",
        "status": 0,
        "favourites": ["bone", "candy"],
    }
