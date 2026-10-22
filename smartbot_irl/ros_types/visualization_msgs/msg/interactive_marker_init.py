# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .interactive_marker import InteractiveMarker


@dataclass(slots=True)
class InteractiveMarkerInit:
    server_id: str = ""
    seq_num: int = 0
    markers: list[InteractiveMarker] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "visualization_msgs/msg/InteractiveMarkerInit"


__all__ = ["InteractiveMarkerInit"]