# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Any, Union


__all__ = ["_validate_path_format", "_validate_path_type"]


_VALID_FORMATS = {"json", "yaml"}


def _validate_path_format(path: Path, target: Union[str, None] = None) -> str:
    format = path.suffix[1:]  # "foo/bar.json" -> "json"
    if format not in _VALID_FORMATS:
        raise ValueError
    elif isinstance(target, str):
        if target not in _VALID_FORMATS or target != format:
            raise ValueError
    elif target is not None:
        raise TypeError
    return format


def _validate_path_type(path: Any) -> Path:
    if not isinstance(path, (str, PathLike, Path)):
        raise TypeError
    return Path(path)
