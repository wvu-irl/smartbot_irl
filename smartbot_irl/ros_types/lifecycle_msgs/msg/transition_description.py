# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .state import State
from .transition import Transition


@dataclass(slots=True)
class TransitionDescription:
    transition: Transition = field(default_factory=Transition)
    start_state: State = field(default_factory=State)
    goal_state: State = field(default_factory=State)


    __msgtype__: ClassVar[str] = "lifecycle_msgs/msg/TransitionDescription"


__all__ = ["TransitionDescription"]