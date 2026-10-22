# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .goal_id import GoalID


@dataclass(slots=True)
class GoalStatus:
    goal_id: GoalID = field(default_factory=GoalID)
    status: int = 0
    text: str = ""

    PENDING: ClassVar[int] = 0
    ACTIVE: ClassVar[int] = 1
    PREEMPTED: ClassVar[int] = 2
    SUCCEEDED: ClassVar[int] = 3
    ABORTED: ClassVar[int] = 4
    REJECTED: ClassVar[int] = 5
    PREEMPTING: ClassVar[int] = 6
    RECALLING: ClassVar[int] = 7
    RECALLED: ClassVar[int] = 8
    LOST: ClassVar[int] = 9

    __msgtype__: ClassVar[str] = "actionlib_msgs/msg/GoalStatus"


__all__ = ["GoalStatus"]