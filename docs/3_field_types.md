# Field types

Gata supports most of standard library types, but in some cases this might not be sufficient.
That's why you can either implement your own custom type or use one of predefined types that are
part of `gata.typing` module.

## Supported standard library types

### Primitive types

#### `bool`

Accepts `True`, `False` values as well as falsy and truthy expressions. 
While serialisaion/deserialisation phase value is being cast to boolean.

#### `int`, `float`, `str`

Accepts values as they are, while serialisation/deserialisation int/float/str functions are used to convert values
(this may cause dataloss).

#### `bytes`

Accepts `bytes` values or base64 encoded strings, while serialisation `bytes` values are returned as base64 encoded string,
during deserialisation base64 encoded strings are turned into bytes.

### Date-related types

#### `datetime.date`

Accepts string containing valid ISO-8601 representation or `datetime.date` instances, while serialisation converts
`datetime.date` instance to string containing valid ISO-8601 date representation.

#### `datetime.datetime`
Same as `datetime.date` but accepts valid ISO-8601 datetime representation.


#### `datetime.time`
Same as `datetime.date` but accepts valid ISO-8601 time representation.


#### `datetime.timedelta`
Same as `datetime.date` but accepts valid ISO-8601 time representation.

### Other standard library types

#### `decimal.Decimal`
Accepts string that can be converted to `decimal.Decimal` value, while serialisation converts value to string.

#### `uuid.UUID`
Accepts string that can be converted to `uuid.UUID` value, while serialisation converts value to string.

#### `enum.Enum`
Accepts value that can be converted to valid instance of subclass of `enum.Enum`, while serialisation converts value to either string or integer.

#### `ipaddress.IPv4Address`
Accepts string that is valid ipv4 address representation, while serialisation converts value to string.

#### `ipaddress.IPv6Address`
Accepts string that is valid ipv6 address representation, while serialisation converts value to string.

### Typing library

#### `typing.Any`
Accepts any value, while serialisation the value is returned as-is.

#### `typing.List` with defined subtype
Accepts values that can be converted to list with specified type, while serialisation converts value to list of converted type.

#### `typing.Tuple` with defined subtype
Same as `typing.List`, but value is converted to tuple.

#### `typing.Set` with defined subtype
Same as `typing.List`, but value is converted to set.

#### `typing.FrozenSet` with defined subtype
Same as `typing.List`, but value is converted to frozen-set.

#### `typing.TypedDict`
Accept dict which values validates against defined schema.

#### `typing.Optional`
Accept value of all supported types with optional modifier.

#### `typing.Union`
Accept value that is one of specified type in the union type. While deserialisation gata will try to assert the type
that field names matches most of defined key names in passed serialised value. 

### Dataclasses
All dataclasses are supported and they are validated against defined schema, while serialisation 
they are converted to dict value containing converted types.

## Defining custom types

The following example defines custom type for validating and representing UK post codes

```python
import re
from typing import Any

from gata import dataclass, Type
from gata.errors import ValidationError

UK_POST_CODE_REGEX = re.compile(
    "^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([AZa-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$"
)


class UKPostCode(Type):
    def __init__(self, value: Any):
        self.value = str(value)

    def validate(self) -> Any:
        if UK_POST_CODE_REGEX.match(self.value):
            return self.value
        raise ValidationError(f"passed value {self.value} is not valid uk post code")

    def serialise(self) -> Any:
        return self.value


@dataclass
class User:
    name: str
    post_code: UKPostCode
    age: int


bob = User(name="Bob", post_code="SW16 5QW", age=22)

try:
    failed_tom = User(name="Tom", post_code="123111", age=28)
except ValidationError as error:
    ...

# file://examples/custom_type.py
```
