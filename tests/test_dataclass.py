from gata import DataClass


def test_can_define_class():

    class Example(DataClass):
        name: str = "John"
        age: int

    assert issubclass(Example, DataClass)
    assert hasattr(Example, "validate")
    assert hasattr(Example, "create")
    assert hasattr(Example, "__schema__")
