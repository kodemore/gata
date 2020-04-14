from dataclasses import dataclass
from typing import List

from gata import transform


def test_transform_object() -> None:
    @dataclass
    class UserInterest:
        name: str

    @dataclass
    class UserEntity:
        user_name: str
        user_email: str
        user_id: int
        interests: List[UserInterest]

    @dataclass
    class UserResource:
        user_name: str
        email: str
        id: int
        interests: List[str]

    user_entity = UserEntity(
        user_name="Bob", user_email="bob@email.com", user_id=12, interests=[UserInterest(name="baseball")],
    )

    user_resource = transform(
        user_entity, UserResource, {"user_email": "email", "user_id": "id", "interests": {"$item": "name"}},
    )

    assert isinstance(user_resource, UserResource)
    assert user_resource.user_name == user_entity.user_name
    assert user_resource.email == user_entity.user_email
    assert user_resource.id == user_entity.user_id
