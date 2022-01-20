# -*- coding: utf-8 -*-

from dataclasses import is_dataclass
from dataclasses_io.core import get_config


__all__ = ["dataclass_io"]


def _process_class(cls):
    if is_dataclass(cls):
        setattr(cls, "config", property(get_config, None, None, None))
    return cls


def dataclass_io(cls=None):
    def wrap(cls):
        return _process_class(cls)

    if cls is None:
        return wrap
    return wrap(cls)
