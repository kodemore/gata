# Gata [![Build Status](https://travis-ci.org/kodemore/gata.svg?branch=master)](https://travis-ci.org/kodemore/gata) [![codecov](https://codecov.io/gh/kodemore/gata/branch/master/graph/badge.svg)](https://codecov.io/gh/kodemore/gata) [![Maintainability](https://api.codeclimate.com/v1/badges/00892e0c37a7f1716bdd/maintainability)](https://codeclimate.com/github/kodemore/gata/maintainability)
Gata is a toolbox library for python's dataclasses which allows to serialise/deserialise/validate complex dataclasses.

# Introduction

## Installation

`pip install gata`

## Features
 - non-intrusive interface
 - dataclasses validation mechanism
 - support for complex datatypes
 - serialisation/deserialisation mechanism
 - easy to use field mapping
 - custom serialisation/deserialisation

### Validating dataclass
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import gata


@dataclass
class Pet:
    name: str = field(default="Pimpek")
    age: int = field(default=0)
    tags: List[str] = field(default_factory=list)
    sold_at: Optional[datetime] = field(default=None)

gata.validate({
    "name": "Boo",
    "age": 10,
    "tags": []
}, Pet) # returns True
```

### Serialising dataclasses
Gata serialisation mechanism is a better alternative to well known `dataclasses.asdict` function. 
Differences between `gata`'s serialiser and `asdict` function are:
 - `gata` ensures that returned value matches annotated type 
 - `gata` knows how to serialise datetime values, sets, typed lists, typed sets, typed dicts, enums and more
 - `gata` gives easy interface to implement custom serialisers for your custom defined types

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

### Deserialising into dataclasses
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

pet = gata.deserialise({"name": "Boo", "age": 10, "tags": [], "sold_at": None}, Pet) 
```

### Useful decorators
If you prefer more OOP approach you can use `gata.serialisable`, `gata.valiadatable` decorators, consider the following example
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from gata import serialisable, validatable

@validatable
@serialisable
class Pet:
    name: str
    age: int = field(default=0)
    tags: List[str] = field(default_factory=list)
    sold_at: Optional[datetime] = field(default=None)

# Deserialise Pet
pet = Pet.deserialise({"name": "Boo", "age": 10, "tags": [], "sold_at": None}) 

# Serialise Pet
pet.serialise()

# Validate dict against Pet's schema
Pet.validate({"name": "Boo", "age": 10, "tags": [], "sold_at": None})
```

> Note: `@dataclass` decorator is not required when using `serialisable` or `validatable` decorators, as gata automatically converts decorated class into dataclass.


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
        name = Field(min=2, max=10)  # Minimum name length is 2 maximum is 10
        age = Field(min=0, max=100)  # Minimum pet's age is 0 and maximum is 100
        tags = Field(min=1)  # List of tags must contain at least one item
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
        name = Field(min=2, max=10, serialiser=lambda name: name.strip()) # serialiser set directly in Field
        
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
 
## Supported python types

The following is a comprehensive list of supported python types.

### Primitive types

#### `bool`

Accepts boolean values, while serialisaion/deserialisation cast to boolean, accepts also truthy or falsy expressions. 

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

### Standard library

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
Accept value that is one of specified type in the union type.

### Dataclasses
All dataclasses are supported and they are validated against defined schema, while serialisation they are converted to dict value 
containing converted types. 

## Validators

`Gata` also provides interface for simple validation.

### List of available validators

 - `Validator.array(value, items)` checks if value is set or list and each item conforms passed validator
 - `Validator.base64(value)` checks if passed string is valid base64 value
 - `Validator.date(value, min, max)` checks if passed string is valid iso date value
 - `Validator.datetime(value, min, max)` checks if passed string is valid iso datetime value
 - `Validator.email(value)` checks if passed string is valid email address
 - `Validator.falsy(value)` checks if passed string is valid falsy expression
 - `Validator.hostname(value)` checks if passed string is valid host name
 - `Validator.ipv4(value)` checks if passed string is valid ipv4 address
 - `Validator.ipv6(value)` checks if passed string is valid ipv6 address
 - `Validator.number(value, min, max, multiple_of)` checks if passed value is a valid number
 - `Validator.object_id(value)` checks if passed string is valid bson's object_id value
 - `Validator.semver(value)` checks if passed string is valid semantic versioning number
 - `Validator.time(value, min, max)` checks if passed string is valid iso time
 - `Validator.truthy(value)` checks if passed string is valid truthy expression
 - `Validator.uri(value)` checks if passed string is valid uri
 - `Validator.url(value)` checks if passed string is valid url
 - `Validator.uuid(value)` checks if passed string is valid uuid number
