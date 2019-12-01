from gata import DataClass


class Example(DataClass):
    name: str = "John"

    def __init__(self, name: str):
        self.name = name


n = Example(name="Tom")
