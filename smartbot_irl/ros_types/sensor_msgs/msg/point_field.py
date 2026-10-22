# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class PointField:
    name: str = ""
    offset: int = 0
    datatype: int = 0
    count: int = 0

    INT8: ClassVar[int] = 1
    UINT8: ClassVar[int] = 2
    INT16: ClassVar[int] = 3
    UINT16: ClassVar[int] = 4
    INT32: ClassVar[int] = 5
    UINT32: ClassVar[int] = 6
    FLOAT32: ClassVar[int] = 7
    FLOAT64: ClassVar[int] = 8

    __msgtype__: ClassVar[str] = "sensor_msgs/msg/PointField"


__all__ = ["PointField"]