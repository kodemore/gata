from gata.types import String


def test_can_instantiate():
    test_instance = String()
    assert test_instance.validate("a") is None


def test_validate_normal_string():
    test_instance = String()
    assert test_instance.validate("test") is None
