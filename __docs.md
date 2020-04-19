
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import gata


@dataclass
class Pet:
    name: str
    age: int = field(default=0)
    tags: List[str] = field(default_factory=list)
    sold_at: Optional[datetime] = field(default=None)

pet = Pet(name="Boo", age=10)

gata.serialisable(pet)  # {"name": "Boo", "age": 10, "tags": [], "sold_at": None}
```

#### Mapping fields in the result
Serialise method can be fetched with additional `mapping` parameter which tells serialisation mechanism to rename fields
accordingly to set mapping rules in the returned result. Consider following example:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import gata


@dataclass
class Pet:
    name: str
    age: int = field(default=0)
    tags: List[str] = field(default_factory=list)
    sold_at: Optional[datetime] = field(default=None)

pet = Pet(name="Boo", age=10)

gata.serialisable(pet, mapping={
    "name": "pet_name", # name field will be mapped to `pet_name`
    "tags": False, # tags field will be excluded from serialisation
    # rest of the fields will be returned with names taken from dataclass
})
```

`mapping` argument must be a dict of `Dict[str, Union[str, bool, callable, dict]]` type.

##### Mapping behaviour
When value is a `string`, field name will be simply mapped to corresponding key value.

When value is a `bool(False)` field will not be returned in the serialised value.

When value is a `callable`, value corresponding to mapped key will be passed to callable, which should return tuple.
First tuple's item will be used as a key for returned value and second is the value that will get returned as a part of serialised object.

Nested mapping is allowed, by passing `Dict[str, Union[str, bool, callable, dict]]` instance as a key value.

##### Nested mapping
```python
from dataclasses import dataclass
from typing import List

import gata

@dataclass
class Pet:
    name: str
    age: int


@gata.serialisable
class PetStore:
    name: str
    pets: List[Pet]

boo = Pet(name="Boo", age=10)
noo = Pet(name="Noo", age=20)

store = PetStore(name="Happy Pets", pets=[boo, noo])

store.serialise(
    name="store_name",  # corresponds to PetStore.name property
    pets={
        "$self": "pet_list",  # corresponds to PetStore.pets property
        "name": "pet_name", # corresponds to Pet.name property
        "age": False # corresponds to Pet.age property
    }
)
```

> Note: When using custom serialising methods, only field to field mapping is available.


### Adding schema to validators
Schema can be used for more precise validation rules, eg. validating string length and/or format.
Consider the following example:

```python
from datetime import datetime
from enum import Enum
from typing import List
from dataclasses import dataclass
from gata import Field

class PetStatus(Enum):
    AVAILABLE = 0
    PENDING = 1
    BOOKED = 2
    SOLD = 3

@dataclass()
class Pet:
    sold_at: datetime
    tags: List[str]
    name: str = "Pimpek"
    age: int = 0
    status: PetStatus = PetStatus.AVAILABLE

    class Schema:
        name = Field(minimum=2, maximum=10)  # Minimum name length is 2 maximum is 10
        age = Field(minimum=0, maximum=100)  # Minimum pet's age is 0 and maximum is 100
        tags = Field(minimum=1)  # List of tags must contain at least one item
```
Inner `Schema` class contains properties, name of the property corresponds to parent class.
Each property must be Field instance. Field constructor accepts following arguments:

 - `min: int` - depending on the context it specified be min value or length
 - `max: int` - depending on the context it specifies maximum value or length
 - `string_format: str` - used to specify accepted string's format, available list of formats is available below
 - `multiple_of: typing.Union[int, float]` - used with numbers to specify that validated value has to be multiplication of given value
 - `pattern: str` - specifies regex used to validate string value
 - `read_only: bool` - sets property to read_only mode, which means property will be serialised as usual but skipped during deserialisation and validation if not set
 - `write_only: bool` - sets property to write_only mode, which means property will be deserialised and validated but not serialised
 - `serialiser: typing.Callable` - allows to override standard serialiser for property
 - `deserialiser: typing.Callable` - allows to override standard deserialiser for property

#### Custom serialisers/deserialisers in schema

In case creating custom serialisable type is not an option gata provides simple api for defining
custom serialisation/deserialisation functions for properties.

Please consider following example:
```python
from typing import List
from dataclasses import dataclass
from gata import Field
from bson import ObjectId

@dataclass()
class Pet:
    id: ObjectId
    tags: List[str]
    name: str = "Boo"
    age: int = 0

    class Schema:
        name = Field(minimum=2, maximum=10, serialiser=lambda name: name.strip()) # serialiser set directly in Field

        # serialiser and deserialiser defined as schema methods
        @staticmethod
        def serialise_id(pet_id: ObjectId) -> str:
            return str(pet_id)

        @staticmethod
        def deserialise_id(pet_id: str) -> ObjectId:
            return ObjectId(pet_id)
```

In the above example default serialiser/deserialiser for `id` property has been replaced with methods `serialise_id` and
`deserialise_id`, keep in mind that naming here is not accidental.

Property serialisers in `Schema` class must be prefixed with `serialise_` prefix, deserialisers accordingly with `deserialise_` prefix.
Serialisation and desarialisation MUST be static methods.

### Available string formats (string validators)
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
