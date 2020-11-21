import pytest


def test_valid_values():
    try:
        from bson import ObjectId

    except ImportError:
        pytest.skip("Bson not intalled")

    from gata.bson_support import validate_object_id

    assert validate_object_id("507f1f77bcf86cd799439011")
    assert validate_object_id(ObjectId())
