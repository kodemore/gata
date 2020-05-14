import pytest

from gata.errors import ValidationError
from gata.validators import validate_uuid


@pytest.mark.parametrize(
    "value",
    (
        "cff801a5-5db7-4287-9414-64ba51a9a730",
        "ad047288-b643-4cd0-8c79-354f68140bef",
        "b11b1836-ad3e-4944-9c80-eaccdac0487b",
        "e643c4f2-f9c1-4287-b465-1e02ba7d902d",
        "57766d9b-9ea2-4740-9b26-56dfdd79678a",
        "c8a73edc-117f-4a97-a1fa-a5cb84e78bd3",
        "ffcd057d-8df6-4cc4-9f68-191a129d46a7",
        "479908f7-4004-4671-9608-6a6672028db3",
        "5b92ff61-c940-4771-8a35-7dab65d43f29",
        "bb2e4878-4bb2-440d-90ef-ba2724c1e8c2",
    ),
)
def test_valid_values(value: str):
    assert validate_uuid(value)


@pytest.mark.parametrize(
    "value",
    (
        1,
        2,
        "ad23rfw"
    ),
)
def test_invalid_values(value: str):
    with pytest.raises(ValidationError):
        validate_uuid(value)
