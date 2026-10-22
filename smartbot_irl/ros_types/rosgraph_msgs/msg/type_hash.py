# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class TypeHash:
    version: int = 1
    value: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.zeros(32, dtype=numpy.uint8))


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/TypeHash"


__all__ = ["TypeHash"]