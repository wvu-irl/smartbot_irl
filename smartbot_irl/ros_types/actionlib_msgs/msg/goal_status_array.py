# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .goal_status import GoalStatus
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class GoalStatusArray:
    header: Header = field(default_factory=Header)
    status_list: list[GoalStatus] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "actionlib_msgs/msg/GoalStatusArray"


__all__ = ["GoalStatusArray"]