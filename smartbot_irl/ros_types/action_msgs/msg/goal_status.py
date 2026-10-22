# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .goal_info import GoalInfo


@dataclass(slots=True)
class GoalStatus:
    goal_info: GoalInfo = field(default_factory=GoalInfo)
    status: int = 0

    STATUS_UNKNOWN: ClassVar[int] = 0
    STATUS_ACCEPTED: ClassVar[int] = 1
    STATUS_EXECUTING: ClassVar[int] = 2
    STATUS_CANCELING: ClassVar[int] = 3
    STATUS_SUCCEEDED: ClassVar[int] = 4
    STATUS_CANCELED: ClassVar[int] = 5
    STATUS_ABORTED: ClassVar[int] = 6

    __msgtype__: ClassVar[str] = "action_msgs/msg/GoalStatus"


__all__ = ["GoalStatus"]