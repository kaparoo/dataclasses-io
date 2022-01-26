# -*- coding: utf-8 -*-

from dataclasses_io.utils import _validate_path_format, _validate_path_type

import json
import yaml

from os import PathLike
from pathlib import Path
from typing import Optional, Literal, Union


__all__ = [
    "get_config",
    "save",
    "save_json",
    "save_yaml",
    "load",
    "load_json",
    "load_yaml",
]


FormatType = Literal["json", "yaml"]
PathType = Union[str, Path, PathLike]


def get_config(self):
    fields = (field for field in self.__dataclass_fields__)
    return {field: getattr(self, field) for field in fields}


def save(
    self,
    path: PathType,
    overwrite: bool = False,
    encoding: Optional[str] = None,
    format: Optional[FormatType] = None,
):
    path = _validate_path_type(path)
    if path.exists() and not path.is_file():
        raise FileExistsError("not regular file: %s" % path)

    format = _validate_path_format(path, format)

    root = path.parent
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)

    cls_name = self.__class__.__name__
    contents = {cls_name: self.config}

    if path.is_file():
        with path.open("r", encoding=encoding) as file:
            file_data = {}
            if format == "json":
                file_data = json.load(file)
            elif format == "yaml":
                file_data = yaml.load(file, Loader=yaml.FullLoader)
            if cls_name not in file_data or overwrite:
                contents = {**file_data, **contents}

    with path.open("w", encoding=encoding) as file:
        if format == "json":
            json.dump(contents, file, indent=4)
        elif format == "yaml":
            yaml.dump(contents, file, indent=4)


def save_json(
    self,
    path: PathType,
    overwrite: bool = False,
    encoding: Optional[str] = None,
):
    self.save(path, overwrite, encoding, format="json")


def save_yaml(
    self,
    path: PathType,
    overwrite: bool = False,
    encoding: Optional[str] = None,
):
    self.save(path, overwrite, encoding, format="yaml")


@classmethod
def load(
    cls,
    path: PathType,
    encoding: Optional[str] = None,
    format: Optional[FormatType] = None,
):
    path = _validate_path_type(path)
    if not path.exists():
        raise FileNotFoundError("no such file %s" % path)
    elif not path.is_file():
        raise FileExistsError("not regular file: %s" % path)

    format = _validate_path_format(path, format)
    with path.open("r", encoding=encoding) as file:
        file_data = {}
        if format == "json":
            file_data = json.load(file)
        elif format == "yaml":
            file_data = yaml.load(file, Loader=yaml.FullLoader)
        file_data = file_data[cls.__name__]
        kwargs = {k: v for k, v in file_data.items()}
        return cls(**kwargs)


@classmethod
def load_json(cls, path: PathType, encoding: Optional[str] = None):
    return cls.load(path, encoding, format="json")


@classmethod
def load_yaml(cls, path: PathType, encoding: Optional[str] = None):
    return cls.load(path, encoding, format="yaml")
