# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class CustomPoint:
    offset_time: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    reflectivity: int = 0
    tag: int = 0
    line: int = 0


    __msgtype__: ClassVar[str] = "livox_ros_driver2/msg/CustomPoint"


__all__ = ["CustomPoint"]