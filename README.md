# Gata
Extended data classes for python with json-schema like validation support

# Introduction

## Installation

## Features
 - dataclasses with built-in value validation
 - support for complex nested validation
 - over 15 validators for everyday use
 - mapping support 


## Dataclasses
Dataclasses are containers and validators for data used by other classes. It is providing simple interface for 
setting/getting/validating value. `Gata` library can be used with python built-in types, which is recommended for
fast prototyping and very simple validation but also provide powerful type objects that are reflecting json schema 
compatible types.

### Dataclass example with python built-in types
```python
from gata import DataClass
from datetime import datetime


class Pet(DataClass):
    name: str = "Pimpek"
    age: int = 0
    sold_at: datetime
    tags: dict
    status: int = 0
```

### Dataclass with json validators

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
    name: types.String(min=2, max=12) = "Pimpek" # Minimum length of a string is 2 and maximum is 12
    age: types.Integer(min=0, max=200) = 0
    sold_at: types.DateTime()
    tags: type.Array[types.String(min=2, max=100)]
    status: PetStatus = PetStatus.AVAILABLE
```

## Python types to json types mapping table

| python type | maps to | description | 
|:--:|:--:|:--:|
|`int`|`gata.types.Integer`|Validates integer numbers|
|`bool`|`gata.types.Boolean`|Validates boolean values|
|`str`|`gata.types.String`|Validates strings|
|`float`|`gata.types.Number`|Validates number|
|`bytes`|`gata.types.String[gata.types.Format.BYTES]`|Validates bytes|
|`dict`|n/a|Not supported|
|`list`|`gata.types.Array[Any]`|Validates arrays values|
|`tuple`|`gata.types.Array[Any]`|Validates arrays values|
|`set`|`gata.types.Array(unique=True)`|Validates unique arrays values|
|`typing.Dict`|n/a|Not supported|
|`typing.List`|`gata.types.Array[Any]`|Same as `list`|
|`typing.List[str]`|`gata.types.Array[gata.types.String]`|Same as `list`|
|`datetime.datetime`|`gata.types.String[gata.types.Format.DATETIME]`| Validates iso compatible datetime values|
|`datetime.date`|`gata.types.String[gata.types.Format.DATE]`| Validates iso compatible date values|
|`datetime.time`|`gata.types.String[gata.types.Format.TIME]`| Validates iso compatible time values|

## Types reference

### Array

### Boolean

### Enum

### Integer

### Number

### Object

### String


## Validators reference

### base64 validator

### date validator

### datetime validator

### email validator

### falsy validator

### truthy validator

### hostname validator

### ipv4 validator

### ipv6 validator

### length validator

### multiple of validator

### range validator

### semver validator

### time validator

### truthy validator

### uri validator

### url validator

### uuid validator
