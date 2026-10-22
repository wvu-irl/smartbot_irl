# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class MultiArrayDimension:
    label: str = ""
    size: int = 0
    stride: int = 0


    __msgtype__: ClassVar[str] = "std_msgs/msg/MultiArrayDimension"


__all__ = ["MultiArrayDimension"]