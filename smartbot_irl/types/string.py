from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List

from smartbot_irl.ros_types.std_msgs.msg import String as RosString

from .base_type import BaseType


@dataclass
class String(BaseType):
    ros_type = 'std_msgs/String'
    data: str = ''

    @classmethod
    def from_ros(cls, msg: RosString):
        return cls(data=msg.data)

    def to_ros(self):
        return {'data': self.data}
