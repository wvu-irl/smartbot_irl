# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class RegionOfInterest:
    x_offset: int = 0
    y_offset: int = 0
    height: int = 0
    width: int = 0
    do_rectify: bool = False


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/RegionOfInterest"


__all__ = ["RegionOfInterest"]