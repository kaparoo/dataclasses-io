# -*- coding: utf-8 -*-

from dataclasses import is_dataclass
from dataclasses_io.core import get_config, save_json, load_json


__all__ = ["dataclass_io"]


def _process_class(cls):
    if is_dataclass(cls):
        setattr(cls, "config", property(get_config, None, None, None))
        setattr(cls, "save_json", save_json)
        setattr(cls, "load_json", load_json)
    return cls


def dataclass_io(cls=None):
    def wrap(cls):
        return _process_class(cls)

    if cls is None:
        return wrap
    return wrap(cls)
