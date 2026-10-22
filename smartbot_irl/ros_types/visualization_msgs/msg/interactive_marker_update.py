# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .interactive_marker import InteractiveMarker
from .interactive_marker_pose import InteractiveMarkerPose


@dataclass(slots=True)
class InteractiveMarkerUpdate:
    server_id: str = ""
    seq_num: int = 0
    type: int = 0
    markers: list[InteractiveMarker] = field(default_factory=list)
    poses: list[InteractiveMarkerPose] = field(default_factory=list)
    erases: list[str] = field(default_factory=list)

    KEEP_ALIVE: ClassVar[int] = 0
    UPDATE: ClassVar[int] = 1

    __msgtype__: ClassVar[str] = "visualization_msgs/msg/InteractiveMarkerUpdate"


__all__ = ["InteractiveMarkerUpdate"]