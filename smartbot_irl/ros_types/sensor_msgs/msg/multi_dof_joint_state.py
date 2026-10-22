# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.transform import Transform
from ...geometry_msgs.msg.twist import Twist
from ...geometry_msgs.msg.wrench import Wrench
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class MultiDOFJointState:
    header: Header = field(default_factory=Header)
    joint_names: list[str] = field(default_factory=list)
    transforms: list[Transform] = field(default_factory=list)
    twist: list[Twist] = field(default_factory=list)
    wrench: list[Wrench] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/MultiDOFJointState"


__all__ = ["MultiDOFJointState"]