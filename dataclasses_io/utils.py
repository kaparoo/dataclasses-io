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


def _validate_path_format(path: Path, format: Union[str, None] = None) -> str:
    try:
        path_format = _SUFFIX_TO_FORMAT[path.suffix]
    except KeyError:
        raise ValueError("invalid suffix: %s" % path.suffix)

    if isinstance(format, str):
        if format not in _VALID_FORMATS:
            raise ValueError("`format` must be one of %s" % _VALID_FORMATS)
        elif format != path_format:
            raise ValueError("expected %s file, not %s" % (format, path_format))
    elif format is not None:
        raise TypeError(
            "`format` expected str or NoneType object, not %s"
            % format.__class__.__name__
        )

    return path_format


def _validate_path_type(path: Any) -> Path:
    if not isinstance(path, (str, PathLike, Path)):
        raise TypeError(
            "`path` expected str, os.PathLike or pathlib.Path object, not %s"
            % path.__class__.__name__
        )
    return Path(path)
