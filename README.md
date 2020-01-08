# Gata [![Build Status](https://travis-ci.org/kodemore/gata.svg?branch=master)](https://travis-ci.org/kodemore/gata) [![codecov](https://codecov.io/gh/kodemore/gata/branch/master/graph/badge.svg)](https://codecov.io/gh/kodemore/gata) [![Maintainability](https://api.codeclimate.com/v1/badges/c224b3a0ece5d2005b0c/maintainability)](https://codeclimate.com/github/kodemore/gata/maintainability)
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
setting/getting/validating values. `Gata` library utilises built-in python types (support has some limitations, 
supported list of types is listed below).

Dataclasses can also be used as a serialisation/deserialisation library so you can store your data in easy manner.


### Dataclass example
```python
from typing import Optional, List
from gata import DataClass
from datetime import datetime


class Pet(DataClass):
    name: str = "Pimpek"  # "Pimpek" is a default value for Pet.name
    age: int = 0
    sold_at: Optional[datetime]
    tags: List[str]

Pet.validate({
    "name": "Boo",
    "age": 10,
    "tags": []
}) # returns True

pet = Pet.unserialise({
    "name": "Boo",
    "age": 10,
    "tags": []
}) #  creates Pet instance with validated data

pet.serialise() # serialises pet again to dict
```

### Dataclass validators with meta details

```python
from datetime import datetime
from enum import Enum
from typing import List

from gata import DataClass

class PetStatus(Enum):
    AVAILABLE = 0
    PENDING = 1
    BOOKED = 2
    SOLD = 3


class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    sold_at: datetime
    tags: List[str]
    status: PetStatus = PetStatus.AVAILABLE
    
    class Meta:
        name = {"min": 2, "max": 10}  # Minimum name length is 2 maximum is 10
        age = {"min": 0, "max": 100}  # Minimum pet's age is 0 and maximum is 100
        tags = {"min": 1 , "items": {"min": 2, "max": 10}}  # Minimum amount of tags is 1 and each tag name's length must be between 2 to 10 characters
```
Inner `Meta` class can be used to further specify validation limitations, the following is a list of possible
options that might be used in the meta field's specification:

 - `min` - depending on the context it specified be min value or length
 - `max` - depending on the context it specifies maximum value or length
 - `format` - used to specify accepted string's format, available list of formats is available below
 - `multiple_of` - used with numbers to specify that validated value has to be multiplication of given value
 - `items` - used with lists or sets to specify item's limitation

### Available string formats (string validators)
 - `datetime`
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

### Validating data

```python
pet_dict = {
    "name": "Pimpek",
    "age": 12,
    "sold_at": None,
    "tags": ["dogs", "cute"],
    "status": 0,
}

Pet.validate(pet_dict) # uses dataclass defined in previous example, throws an exception when dict contains invalid values
pet_instance = Pet.unserialise(pet_dict) # creates validated instance of Pet class
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

## Supported python types in dataclass

| python type | description | 
|:--:|:--:|
|`int`|Checks if value is an integer number|
|`bool`|Checks if value is valid boolean value|
|`str`|Checks if value is a string|
|`float`|Checks if value is a number|
|`bytes`|Checks if value if byte64 encoded string|
|subclasses of `enum.Enum`|Checks if value exists within enum definition|
|`datetime.datetime`| Checks if value is iso compatible datetime|
|`datetime.date`|Checks if value is iso compatible date|
|`datetime.time`| Checks if value is iso compatible time|
|`typing.Any`|Validates against everything|
|`typing.List` with specified type |Validates list of values|
|`typing.Set` with specified type |Validates set of values|
|`typing.Union`|Checks if value conforms one of the provided types|

## Validators

`Gata` also provides interface for simple validation.
 
```python
from gata import Validator

# Validate email
Validator.email("test@test.com")
```

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
 - `Validator.semver(value)` checks if passed string is valid semantic versioning number
 - `Validator.time(value, min, max)` checks if passed string is valid iso time
 - `Validator.truthy(value)` checks if passed string is valid truthy expression
 - `Validator.uri(value)` checks if passed string is valid uri
 - `Validator.url(value)` checks if passed string is valid url
 - `Validator.uuid(value)` checks if passed string is valid uuid number


