# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .service import Service
from .topic import Topic


@dataclass(slots=True)
class Action:
    name: str = ""
    send_goal: Service = field(default_factory=Service)
    get_result: Service = field(default_factory=Service)
    cancel_goal: Service = field(default_factory=Service)
    feedback: Topic = field(default_factory=Topic)
    status: Topic = field(default_factory=Topic)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/Action"


__all__ = ["Action"]