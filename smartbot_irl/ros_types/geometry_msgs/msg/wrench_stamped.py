# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .wrench import Wrench
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class WrenchStamped:
    header: Header = field(default_factory=Header)
    wrench: Wrench = field(default_factory=Wrench)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/WrenchStamped"


__all__ = ["WrenchStamped"]