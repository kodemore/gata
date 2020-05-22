# Detailed schema

Sometimes pure python types might not be sufficient enough to validate your data. This is
where schema definition may come in handy. Schema definition is a nested `Schema` class 
defined inside your dataclass, which contains fields definition which names corresponds directly
to your dataclass' field names.

The following code is an example schema definition:

```python
from typing import List, Optional

from gata import field, dataclass, StringFormat


@dataclass
class User:
    email: str = field(string_format=StringFormat.EMAIL)  # validate email field against email format
    name: str = field(minimum=2, maximum=30)  # min name length is 2 characters
    age: int = field(minimum=2, maximum=120, default=0)  # min user's age is 1 maximum is 120
    favourites: Optional[List[str]]

bob = User(email="valid@email.com", name="Bob", age=121)  # gata.errors.FieldError: Field error `age`: Passed value must be lower than set maximum `120`

# file://examples/schema_example.py
```

Now `User` dataclass not only specifies valid types but also string format and maximum and minimum 
allowed boundaries.

## `gata.Field` properties

#### `maximum: Union[int, float, Decimal]`

For numerical values will set maximal value. For strings and lists will set maximum allowed length.

#### `minimum: Union[int, float, Decimal]`

For numerical values will set maximal value. For strings and lists will set maximum allowed length.

#### `multiple_of: Union[int, float, Decimal]`

Ensures that numerical value is multiplication of passed value

#### `string_format: Union[str, Format]`

Ensures if passed string is validating against passed format. Available formats are listed [below](#available-string-formats).

#### `pattern: str`

Ensures that string is matching specified pattern.

#### `read_only: bool`

Sets field to `read_only` mode - during instantiation this field is ignored.

#### `write_only: bool` 

Sets field to `write_only` mode - during serialisation this field is ignored.

#### `serialiser: typing.Callable` 

Overrides field's default serialiser - during serialisation `serialiser` will be called.  

#### `deserialiser: typing.Callable`

Overrides field's default deserialiser - during instantiation `deserialiser` will be called.

#### `default: Any`

Sets default value if none is provided during instantiation.

#### `default_factory: typing.Callable`

Sets default value factor which will be called during instantiation if none value is provided.

#### Available string formats
 - `date-time`
 - `date`
 - `time`
 - `uri`
 - `url`
 - `email`
 - `uuid`
 - `hostname`
 - `ipv4`
 - `ipv6`
 - `truthy`
 - `falsy`
 - `semver`
 - `byte`

### Custom serialisers/deserialisers

If defining custom types is too much hassle for you, you can utilise schema functionality to define custom
serialisers/deserialisers.

Serialiser/deserialiser is just a `typing.Callable` value that can be either set as an argument in `gata.Field` instance 
or a function defined in the schema.

> Field serialisers in `Schema` class must be prefixed with `serialise_` prefix, deserialisers accordingly with `deserialise_` prefix.
> Serialisation and desarialisation methods MUST be declared as @staticmethod

```python
from typing import List

from bson import ObjectId

from gata import Field, dataclass


@dataclass()
class Pet:
    id: ObjectId
    tags: List[str]
    name: str = "Boo"
    age: int = 0

    class Schema:
        name = Field(
            minimum=2, maximum=10, serialiser=lambda name: name.strip()
        )  # serialiser set directly in the Field

        # serialiser and deserialiser defined as schema methods
        @staticmethod
        def serialise_id(pet_id: ObjectId) -> str:
            return str(pet_id)

        @staticmethod
        def deserialise_id(pet_id: str) -> ObjectId:
            return ObjectId(pet_id)

# file://examples/custom_serialiser_deserialiser_example.py
```

In the above example default serialiser/deserialiser for `id` property has been replaced with methods `serialise_id` and
`deserialise_id`. `name` field has its serialiser definition passed to `gata.Field` instance.
