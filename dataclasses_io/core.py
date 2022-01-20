# -*- coding: utf-8 -*-

import json
from pathlib import Path


__all__ = ["get_config"]


def get_config(self):
    fields = (field for field in self.__dataclass_fields__)
    return {field: getattr(self, field) for field in fields}


def save_json(self, path, overwrite: bool = False):
    if (path := Path(path)).suffix != ".json":
        raise ValueError
    if not (root := path.parent).exists():
        root.mkdir(parents=True, exist_ok=True)

    json_key = self.__class__.__name__
    contents = {json_key: self.config}

    if not path.exists():
        with path.open("w", encoding="utf-8") as json_file:
            json.dump(contents, json_file, indent=4)
    elif path.is_file():
        with path.open("r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        if json_key not in json_data or overwrite:
            with path.open("w", encoding="utf-8") as json_file:
                json.dump(json_data | contents, json_file, indent=4)
    else:
        raise FileExistsError


@classmethod
def load_json(cls, path):
    path = Path(path)
    if not (path.is_file() and path.suffix == ".json"):
        raise FileNotFoundError
    else:
        with path.open("r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)[cls.__name__]
            kwargs = {k: v for k, v in json_data.items()}
            return cls(**kwargs)
