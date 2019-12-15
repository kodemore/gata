# Gata [![Build Status](https://travis-ci.org/fatcode/gata.svg?branch=master)](https://travis-ci.org/fatcode/gata) [![codecov](https://codecov.io/gh/fatcode/gata/branch/master/graph/badge.svg)](https://codecov.io/gh/fatcode/gata) [![Maintainability](https://api.codeclimate.com/v1/badges/c224b3a0ece5d2005b0c/maintainability)](https://codeclimate.com/github/fatcode/gata/maintainability)
Extended data classes for python with json-schema like validation support

# Introduction

## Installation

`pip install gata`

## Features
 - dataclasses with built-in value validation
 - support for complex nested validation
 - serialisation/unserialising mechanism


# Dataclasses
Dataclasses are containers and validators for data used by other classes. It is providing simple interface for 
setting/getting/validating values. `Gata` library can be used with python built-in types, which is recommended for
fast prototyping and very simple validation but also provide powerful type objects reflecting json schema 
compatible types.

Dataclasses can also be used as a serialisation/deserialisation library so you can store your data in easy manner.


### Dataclass example with python built-in types
```python
from gata import DataClass
from datetime import datetime


class Pet(DataClass):
    name: str = "Pimpek"  # "Pimpek" is a default value for Pet.name
    age: int = 0
    sold_at: datetime
    tags: dict
    status: int = 0
```

### Dataclass validators

```python
from enum import Enum
from gata import types
from gata import DataClass

class PetStatus(Enum):
    AVAILABLE = 0
    PENDING = 1
    BOOKED = 2
    SOLD = 3


class Pet(DataClass):
    name: types.String(min_length=2, max_length=12) = "Pimpek" # Minimum length of a string is 2 and maximum is 12
    age: types.Integer(minimum=0, maximum=200) = 0
    sold_at: types.DateTime()
    tags: types.Array[types.String(min_length=2, max_length=100)]
    status: PetStatus = PetStatus.AVAILABLE
```

### Validating data

Data can be validated in two ways:
 - by using `Dataclass.validate()` method
 - by using `Dataclass.unserialise()` method

```python
pet_dict = {
    "name": "Pimpek",
    "age": 12,
    "sold_at": None,
    "tags": ["dogs", "cute"],
    "status": 0,
}

Pet.validate(pet_dict) # uses dataclass defined in previous example, throws an exception when dict contains invalid values

pet_instance = Pet.create(pet_dict) # creates validated instance of Pet class
```


### Serialising dataclasses
```python
from enum import Enum
from typing import List

from gata import DataClass

# Definitions

class PetStatus(Enum):
    AVAILABLE = 0
    SOLD = 1
    RESERVED = 2

class Favourite(DataClass):
    name: str
    priority: int = 0
    
    def __init__(self, name: str, priority: int = 0):
        self.name = name
        self.priority = priority

class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    favourites: List[Favourite]
    status: PetStatus = PetStatus.AVAILABLE

    def __init__(self, name: str, age: int = 0, favourites: List[Favourite] = [], status: PetStatus = PetStatus.AVAILABLE):
        self.name = name
        self.age = age
        self.favourites = favourites
        self.status = status    

favourites = [Favourite("Bone toy"), Favourite("Color red")]
boo = Pet("boo", 2, favourites)

assert boo.serialise() == {
    "name": "boo",
    "age": 2,
    "favourites": [{"name": "Bone toy", "priority": "0"}, {"name": "Color red", "priority": 0}],
    "status": 0
}
```

### Unserialising complex data

```python
from enum import Enum
from typing import List

from gata import DataClass

# Definitions

class PetStatus(Enum):
    AVAILABLE = 0
    SOLD = 1
    RESERVED = 2

class Favourite(DataClass):
    name: str
    priority: int = 0

class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    favourites: List[Favourite]
    status: PetStatus = PetStatus.AVAILABLE

# Data deserialisation

roxy = Pet.create({
    "name": "Roxy",
    "favourites": [
        {"name": "bones"}, {"name": "balls"}, {"name": "running", "priority": 1}
    ],
    "status": 2
})

assert isinstance(roxy, Pet)
assert isinstance(roxy.favourites[0], Favourite)
assert isinstance(roxy.favourites[1], Favourite)
assert isinstance(roxy.status, PetStatus)
```

### Limitations
Gata cannot correctly serialise/deserialise `OneOf` and `AnyOf` types, those values are simply assigned to corresponding 
properties. 

## Python types to dataclass types mapping

| python type | maps to | description | 
|:--:|:--:|:--:|
|`int`|`gata.types.Integer`|Checks if value is an integer number|
|`bool`|`gata.types.Boolean`|Checks if value is valid boolean value|
|`str`|`gata.types.String`|Checks if value is a string|
|`float`|`gata.types.Number`|Checks if value is a number|
|`bytes`|`gata.types.String[gata.types.Format.BYTES]`|Checks if value if byte64 encoded string|
|`dict`|n/a|Not supported|
|`list`|`gata.types.Array[Any]`|Checks if value is a valid list|
|`tuple`|`gata.types.Array[Any]`|Same as `list`|
|`set`|`gata.types.Array(unique=True)`|Checks if value is a list with unique items|
|`enum.Enum`|`gata.types.Enum`|Checks if value exists within enum definition|
|`datetime.datetime`|`gata.types.String[gata.types.Format.DATETIME]`| Checks if value is iso compatible datetime|
|`datetime.date`|`gata.types.String[gata.types.Format.DATE]`| Checks if value is iso compatible date|
|`datetime.time`|`gata.types.String[gata.types.Format.TIME]`| Checks if value is iso compatible time|
|`typing.Any`|`gata.types.Any`|Validates against everything|
|`typing.Dict`|n/a|Not supported|
|`typing.List`|`gata.types.Array[gata.types.Any]`|Same as `list`|
|`typing.Union`|`gata.types.AnyOf`|Checks if value conforms one of the provided types|

The following table provides some complex type mapping examples:

| python type | maps to | description | 
|:--:|:--:|:--:|
|`typing.List[int]`|`gata.types.Array[gata.types.Integer]`|Validates against list of integers|
|`typing.Union[int, str]`|`gata.types.AnyOf[gata.types.Integer, gata.types.String]`|Validates against valid integer or string value|
|`typing.List[Pet]`|`gata.types.Array[Pet]`|Validates against list of `Pet` instances|
|`typing.Set[Pet]`|`gata.types.Array[Pet]`|Validates against list of unique `Pet` instances|

# Types reference

All types are supporting following attributes inherited from base `gata.Type` type:

 - `default` sets default value for attribute
 - `deprecated` marks attribute as deprecated 
 - `read_only` sets attribute in read-mode only
 - `write_only` sets attribute in write-mode only

## `gata.types.Any`
Validates against any value.

#### Examples
```python
from gata import DataClass
from gata import types 
import typing


class Example(DataClass):
    example_attribute: types.Any
    python_equivalent: typing.Any
```

#### Attributes
No additional attributes are supported.

## `gata.types.AnyOf`
Validates if value conforms any of the specified subtypes.

#### Examples
```python
from gata import DataClass
from gata import types 
import typing


class Example(DataClass):
    example_attribute: types.AnyOf[types.String, types.Number]
    python_equivalent: typing.Union[str, float]
```

#### Attributes
No additional attributes are supported.

## `gata.types.Array`
Validates if value is iterable and each item conforms specified type.

#### Examples
```python
from gata import DataClass
from gata import types 
import typing


class BasicExample(DataClass):
    example_attribute: types.Array[types.Number]
    python_equivalent: typing.List[float]

class UniqueItemsExample(DataClass):
    example_attribute: types.Array(items=types.Number, unique_items=True)
    python_equivalent: typing.Set[float]
```

#### Attributes
 - `items` sets validator per list's item
 - `max_length` sets maximum allowed list's length
 - `min_length` sets minimum allowed list's length
 - `unique_items` all items should be unique

### `gata.types.Boolean`
Validates if value is iterable and each item conforms specified type.

#### Examples
```python
from gata import DataClass
from gata import types 
import typing


class BasicExample(DataClass):
    example_attribute: types.Array[types.Number]
    python_equivalent: typing.List[float]

class UniqueItemsExample(DataClass):
    example_attribute: types.Array(items=types.Number, unique_items=True)
    python_equivalent: typing.Set[float]
```

#### Attributes
 - `items` sets validator per list's item
 - `max_length` sets maximum allowed list's length
 - `min_length` sets minimum allowed list's length
 - `unique_items` all items should be unique

## `gata.types.Enum`
Validates if value is within specified enum values.

#### Examples
```python
from gata import DataClass
from gata import types
from enum import Enum
import typing

class Numbers(Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"

class BasicExample(DataClass):
    example_attribute: types.Enum["one", "two", "three"]
    python_equivalent: Numbers
```

#### Attributes
 - `values` list of valid values


## `gata.types.Integer`
Validates integer values.

#### Examples
```python
from gata import DataClass
from gata import types

class BasicExample(DataClass):
    example_attribute: types.Integer
    python_equivalent: int
```

#### Attributes
 - `minimum` sets minimal valid value (inclusive)
 - `maximum` sets maximum valid value (inclusive)
 - `multiple_of` restricts value to a multiple of a given number


## `gata.types.Null`
Validates `None` values.

This type is mostly to map python's optional types, should not be used per se.

#### Attributes
No additional attributes are supported.


## `gata.types.Number`
Validates integer values.

#### Examples
```python
from numbers import Number
from numbers import Rational
from numbers import Real
import typing

from gata import DataClass
from gata import types

class BasicExample(DataClass):
    example_attribute: types.Number
    python_equivalent: typing.Union[float, int, Number, Real, Rational]
```

#### Attributes
 - `minimum` sets minimal valid value (inclusive)
 - `maximum` sets maximum valid value (inclusive)
 - `multiple_of` restricts value to a multiple of a given number


## `gata.types.OneOf`
Validates if value conforms only one of the specified subtypes.

#### Examples
```python
from gata import DataClass
from gata import types 


class Example(DataClass):
    example_attribute: types.OneOf[types.String, types.Number]
    no_python_equivalent_available = None
```

#### Attributes
No additional attributes are supported.


## `gata.types.String`
Validates if value is valid string.

#### Examples
```python
from gata import DataClass
from gata import types 
from datetime import datetime
from datetime import date
from datetime import time


class Example(DataClass):
    simple_value: types.String
    simple_python: str
    
    datetime_value: types.String(string_format=types.string.Format.DATETIME)
    datetime_python: datetime

    date_value: types.String(string_format=types.string.Format.DATE)
    date_python: date

    time_value: types.String(string_format=types.string.Format.TIME)
    time_python: time

    time_value: types.String(string_format=types.string.Format.BYTE)
    time_python: bytes
```

#### Attributes
 - `string_format` specifies accepted format, list of valid formats is available below
 - `min_length` specified minimum length for a string
 - `max_length` specifies maximum length for a string
 - `pattern` specifies regex pattern which is used to validate the string

#### Available formats (string validators)
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
