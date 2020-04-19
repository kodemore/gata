# Introduction

Data validation serialisation/deserialisation library which plays nicely with built-in python dataclasses. Non-intrusive 
interface allows you to ditch library in every moment and also to introduce library to your code base with minimal effort.

Unlike other libraries, there is no configuration to learn, no schema's micro language, 
just use built-in python's typing library.

#### Example

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0
    sold_at: Optional[datetime] = None

# file://examples/basic_usage.py
```
