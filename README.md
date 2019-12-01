# Gata
Extended data classes for python with json-schema like validation support

# Introduction

## Installation

## Examples

### Simple validator
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

### Complex validator

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

## Supported python types

| python type | maps to | description | 
|:--:|:--:|:--:|
|`int`|`gata.types.Integer`|Validates integer numbers|
|`bool`|`gata.types.Boolean`|Validates boolean values|
|`str`|`gata.types.String`|Validates strings|
|`float`|`gata.types.Number`|Validates number|
|`dict`|n/a|Not supported|
|`list`|`gata.types.Array[Any]`||

## Validators

### Array

### Boolean

### Enum

### Integer

### Number

### Object

### String
