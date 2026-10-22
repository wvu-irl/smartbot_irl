# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .joy_feedback import JoyFeedback


@dataclass(slots=True)
class JoyFeedbackArray:
    array: list[JoyFeedback] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/JoyFeedbackArray"


__all__ = ["JoyFeedbackArray"]