# -*- coding: utf-8 -*-

from dataclasses import is_dataclass
from dataclasses_io.core import (
    get_config,
    save,
    save_json,
    save_yaml,
    load,
    load_json,
    load_yaml,
)


__all__ = ["dataclass_io"]


def _process_class(cls):
    if is_dataclass(cls):
        setattr(cls, "config", property(get_config))
        setattr(cls, "save", save)
        setattr(cls, "save_json", save_json)
        setattr(cls, "save_yaml", save_yaml)
        setattr(cls, "load", load)
        setattr(cls, "load_json", load_json)
        setattr(cls, "load_yaml", load_yaml)
    return cls


def dataclass_io(cls=None):
    """Supports save/load APIs for dataclasses."""

    def wrap(cls):
        return _process_class(cls)

    if cls is None:
        return wrap
    return wrap(cls)
