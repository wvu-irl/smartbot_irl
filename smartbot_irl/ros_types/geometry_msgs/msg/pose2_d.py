# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Pose2D:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Pose2D"


__all__ = ["Pose2D"]