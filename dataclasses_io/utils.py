# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Any, Union


__all__ = ["_validate_path_format", "_validate_path_type"]


_VALID_FORMATS = {"json", "yaml"}


_SUFFIX_TO_FORMAT = {
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
}


def _validate_path_format(path: Path, target: Union[str, None] = None) -> str:
    try:
        format = _SUFFIX_TO_FORMAT[path.suffix]
    except KeyError:
        raise ValueError

    if isinstance(target, str):
        if target not in _VALID_FORMATS or target != format:
            raise ValueError
    elif target is not None:
        raise TypeError
    return format


def _validate_path_type(path: Any) -> Path:
    if not isinstance(path, (str, PathLike, Path)):
        raise TypeError
    return Path(path)
