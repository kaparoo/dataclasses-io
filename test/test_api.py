# -*- coding: utf-8 -*-

from dataclasses import dataclass
from dataclasses_io import dataclass_io
from pathlib import Path


_TEST_PATH = Path(__file__).parent


@dataclass_io
@dataclass
class _MyDataclass:
    id: int
    name: str
    memo: str


if __name__ == "__main__":
    dataclass1 = _MyDataclass(id=42, name="John Doe", memo="Hello, world!")

    # {'id': 42, 'name': 'John Doe', 'memo': 'Hello, world!'}
    print("dataclass1", dataclass1.config)
    dataclass1.save(_TEST_PATH / "test.json")

    dataclass2 = _MyDataclass.load(_TEST_PATH / "test.json")
    print("dataclass2", dataclass2.config)  # same as line 19

    # dataclass1 and dataclass2 have the same properties, but refer to
    # different memories. save() and load() operate well as intended.
    print(f"dataclass1 == dataclass2: {dataclass1 == dataclass2}")
    print(f"dataclass1 is dataclass2: {dataclass1 is dataclass2}")
