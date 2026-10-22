# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .goal_status import GoalStatus


@dataclass(slots=True)
class GoalStatusArray:
    status_list: list[GoalStatus] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "action_msgs/msg/GoalStatusArray"


__all__ = ["GoalStatusArray"]