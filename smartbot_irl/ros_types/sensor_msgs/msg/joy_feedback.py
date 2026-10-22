# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class JoyFeedback:
    type: int = 0
    id: int = 0
    intensity: float = 0.0

    TYPE_LED: ClassVar[int] = 0
    TYPE_RUMBLE: ClassVar[int] = 1
    TYPE_BUZZER: ClassVar[int] = 2

    __msgtype__: ClassVar[str] = "sensor_msgs/msg/JoyFeedback"


__all__ = ["JoyFeedback"]