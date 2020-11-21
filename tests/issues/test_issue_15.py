from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Union

import pytest

from gata import validate_dataclass
from gata.errors import ValidationError


def test_comprehensive_list_validation_with_union() -> None:
    @dataclass
    class TestDataclass:
        emails: List[Union[str, None]]

    td = {"emails": [123]}

    with pytest.raises(ValidationError):
        validate_dataclass(TestDataclass(**td))


def test_comprehensive_list_validation_with_optional() -> None:
    @dataclass
    class TestDataclass:
        emails: List[Optional[str]]

    td = {"emails": [123]}

    with pytest.raises(ValidationError):
        validate_dataclass(TestDataclass(**td))

