# -*- coding: utf-8 -*-

__all__ = ["get_config"]


def get_config(self):
    fields = (field for field in self.__dataclass_fields__)
    return {field: getattr(self, field) for field in fields}
