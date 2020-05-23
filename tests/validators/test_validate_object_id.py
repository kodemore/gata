import pytest

from gata.errors import ValidationError
from gata.validators import validate_object_id
from bson.objectid import ObjectId


@pytest.mark.parametrize(
    "value",
    (
        str(ObjectId()),
        str(ObjectId()),
        str(ObjectId()),
        "507f1f77bcf86cd799439011",
    ),
)
def test_valid_values(value: str):
    assert validate_object_id(value)


@pytest.mark.parametrize(
    "value",
    (
        1,
        True,
        "ad23rfw"
    ),
)
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_object_id(value)
