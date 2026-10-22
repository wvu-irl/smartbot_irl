# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time
from ...unique_identifier_msgs.msg.uuid import UUID


@dataclass(slots=True)
class GoalInfo:
    goal_id: UUID = field(default_factory=UUID)
    stamp: Time = field(default_factory=Time)


    __msgtype__: ClassVar[str] = "action_msgs/msg/GoalInfo"


__all__ = ["GoalInfo"]