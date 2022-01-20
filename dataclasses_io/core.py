# -*- coding: utf-8 -*-

from dataclasses_io.utils import _validate_path_format, _validate_path_type

import json
import yaml

from os import PathLike
from pathlib import Path
from typing import Union


__all__ = [
    "get_config",
    "save",
    "save_json",
    "save_yaml",
    "load",
    "load_json",
    "load_yaml",
]


def get_config(self):
    fields = (field for field in self.__dataclass_fields__)
    return {field: getattr(self, field) for field in fields}


def save(
    self,
    path: Union[str, Path, PathLike],
    encoding: str = "utf-8",
    overwrite: bool = False,
    format: Union[str, None] = None,
):
    path = _validate_path_type(path)
    if path.exists() and not path.is_file():
        raise FileExistsError

    root = path.parent
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)

    cls_name = self.__class__.__name__
    contents = {cls_name: self.config}

    format = _validate_path_format(path, format)
    file_data = {}
    if path.is_file():
        with path.open("r", encoding=encoding) as file:
            if format == "json":
                file_data = json.load(file)
            elif format == "yaml":
                file_data = yaml.load(file, Loader=yaml.FullLoader)
            if cls_name not in file_data or overwrite:
                contents = file_data | contents

    with path.open("w", encoding=encoding) as file:
        if cls_name not in file_data or overwrite:
            contents = file_data | contents
        if format == "json":
            json.dump(contents, file, indent=4)
        elif format == "yaml":
            yaml.dump(contents, file, indent=4)


def save_json(
    self,
    path: Union[str, Path, PathLike],
    encoding: str = "utf-8",
    overwrite: bool = False,
):
    self.save(path, encoding, overwrite, format="json")


def save_yaml(
    self,
    path: Union[str, Path, PathLike],
    encoding: str = "utf-8",
    overwrite: bool = False,
):
    self.save(path, encoding, overwrite, format="yaml")


@classmethod
def load(
    cls,
    path: Union[str, Path, PathLike],
    encoding: str = "utf-8",
    format: Union[str, None] = None,
):
    path = _validate_path_type(path)
    if not path.exists():
        raise FileNotFoundError
    elif not path.is_file():
        raise FileExistsError

    format = _validate_path_format(path, format)
    with path.open("r", encoding=encoding) as file:
        kwargs = {}
        if format == "json":
            file_data = json.load(file)[cls.__name__]
            kwargs = {k: v for k, v in file_data.items()}
        elif format == "yaml":
            file_data = yaml.load(file, Loader=yaml.FullLoader)[cls.__name__]
            kwargs = {k: v for k, v in file_data.items()}
        return cls(**kwargs)


@classmethod
def load_json(cls, path: Union[str, Path, PathLike], encoding: str = "utf-8"):
    return cls.load(path, encoding, format="json")


@classmethod
def load_yaml(cls, path: Union[str, Path, PathLike], encoding: str = "utf-8"):
    return cls.load(path, encoding, format="yaml")
