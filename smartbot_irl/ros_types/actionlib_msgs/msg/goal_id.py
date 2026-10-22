# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time


@dataclass(slots=True)
class GoalID:
    stamp: Time = field(default_factory=Time)
    id: str = ""


    __msgtype__: ClassVar[str] = "actionlib_msgs/msg/GoalID"


__all__ = ["GoalID"]