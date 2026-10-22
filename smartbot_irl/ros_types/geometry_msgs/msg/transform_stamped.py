# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .transform import Transform
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class TransformStamped:
    header: Header = field(default_factory=Header)
    child_frame_id: str = ""
    transform: Transform = field(default_factory=Transform)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/TransformStamped"


__all__ = ["TransformStamped"]