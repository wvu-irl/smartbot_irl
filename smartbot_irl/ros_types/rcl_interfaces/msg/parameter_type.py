# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class ParameterType:
    pass

    PARAMETER_NOT_SET: ClassVar[int] = 0
    PARAMETER_BOOL: ClassVar[int] = 1
    PARAMETER_INTEGER: ClassVar[int] = 2
    PARAMETER_DOUBLE: ClassVar[int] = 3
    PARAMETER_STRING: ClassVar[int] = 4
    PARAMETER_BYTE_ARRAY: ClassVar[int] = 5
    PARAMETER_BOOL_ARRAY: ClassVar[int] = 6
    PARAMETER_INTEGER_ARRAY: ClassVar[int] = 7
    PARAMETER_DOUBLE_ARRAY: ClassVar[int] = 8
    PARAMETER_STRING_ARRAY: ClassVar[int] = 9

    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/ParameterType"


__all__ = ["ParameterType"]