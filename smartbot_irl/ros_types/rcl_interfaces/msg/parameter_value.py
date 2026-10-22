# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class ParameterValue:
    type: int = 0
    bool_value: bool = False
    integer_value: int = 0
    double_value: float = 0.0
    string_value: str = ""
    byte_array_value: list[bytes] = field(default_factory=list)
    bool_array_value: list[bool] = field(default_factory=list)
    integer_array_value: NDArray[numpy.int64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.int64))
    double_array_value: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    string_array_value: list[str] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/ParameterValue"


__all__ = ["ParameterValue"]