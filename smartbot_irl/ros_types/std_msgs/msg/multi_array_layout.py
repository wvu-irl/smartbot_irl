# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .multi_array_dimension import MultiArrayDimension


@dataclass(slots=True)
class MultiArrayLayout:
    dim: list[MultiArrayDimension] = field(default_factory=list)
    data_offset: int = 0


    __msgtype__: ClassVar[str] = "std_msgs/msg/MultiArrayLayout"


__all__ = ["MultiArrayLayout"]