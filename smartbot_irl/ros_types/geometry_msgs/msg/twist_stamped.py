# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .twist import Twist
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class TwistStamped:
    header: Header = field(default_factory=Header)
    twist: Twist = field(default_factory=Twist)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/TwistStamped"


__all__ = ["TwistStamped"]