from gata.types import String
import pytest


def test_can_instantiate():
    test_instance = String()
    assert test_instance.validate("a") is None


def test_validate_normal_string():
    test_instance = String()
    assert test_instance.validate("test") is None


def test_fail_validation():
    test_instance = String()
    with pytest.raises(ValueError):
        test_instance.validate(123)
