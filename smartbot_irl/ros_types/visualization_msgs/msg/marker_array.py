# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .marker import Marker


@dataclass(slots=True)
class MarkerArray:
    markers: list[Marker] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "visualization_msgs/msg/MarkerArray"


__all__ = ["MarkerArray"]