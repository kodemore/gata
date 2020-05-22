from gata.schema import Schema, Field


def test_iterate_over_schema() -> None:
    schema = Schema(str)
    schema["property_a"] = Field()
    schema["property_b"] = Field()
    schema["property_c"] = Field()

    for name, field in schema:
        assert isinstance(name, str)
        assert isinstance(field, Field)
