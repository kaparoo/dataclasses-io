# -*- coding: utf-8 -*-

import json
import yaml
from pathlib import Path


__all__ = ["get_config", "save_json", "load_json", "save_yaml", "load_yaml"]


def get_config(self):
    fields = (field for field in self.__dataclass_fields__)
    return {field: getattr(self, field) for field in fields}


def save_json(self, path, encoding: str = "utf-8", overwrite: bool = False):
    if (path := Path(path)).suffix != ".json":
        raise ValueError
    if not (root := path.parent).exists():
        root.mkdir(parents=True, exist_ok=True)

    json_key = self.__class__.__name__
    contents = {json_key: self.config}

    if not path.exists():
        with path.open("w", encoding=encoding) as json_file:
            json.dump(contents, json_file, indent=4)
    elif path.is_file():
        with path.open("r", encoding=encoding) as json_file:
            json_data = json.load(json_file)
        if json_key not in json_data or overwrite:
            with path.open("w", encoding=encoding) as json_file:
                json.dump(json_data | contents, json_file, indent=4)
    else:
        raise FileExistsError


def save_yaml(self, path, encoding: str = "utf-8", overwrite: bool = False):
    if (path := Path(path)).suffix not in (".yml", ".yaml"):
        raise ValueError
    if not (root := path.parent).exists():
        root.mkdir(parents=True, exist_ok=True)

    yaml_key = self.__class__.__name__
    contents = {yaml_key: self.config}

    if not path.exists():
        with path.open("w", encoding=encoding) as yaml_file:
            yaml.dump(contents, yaml_file, indent=4)
    elif path.is_file():
        with path.open("r", encoding=encoding) as yaml_file:
            yaml_data = yaml.load(yaml_file)
        if yaml_key not in yaml_data or overwrite:
            with path.open("w", encoding=encoding) as yaml_file:
                yaml.dump(yaml_data | contents, yaml_file, indent=4)
    else:
        raise FileExistsError


@classmethod
def load_json(cls, path, encoding: str = "utf-8"):
    path = Path(path)
    if not (path.is_file() and path.suffix == ".json"):
        raise FileNotFoundError
    else:
        with path.open("r", encoding=encoding) as json_file:
            json_data = json.load(json_file)[cls.__name__]
            kwargs = {k: v for k, v in json_data.items()}
            return cls(**kwargs)


@classmethod
def load_yaml(cls, path, encoding: str = "utf-8"):
    path = Path(path)
    if not (path.is_file() and path.suffix in (".yml", ".yaml")):
        raise FileNotFoundError
    else:
        with path.open("r", encoding=encoding) as yaml_file:
            yaml_data = yaml.load(yaml_file)[cls.__name__]
            kwargs = {k: v for k, v in yaml_data.items()}
            return cls(**kwargs)
