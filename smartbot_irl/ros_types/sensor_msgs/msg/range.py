# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Range:
    header: Header = field(default_factory=Header)
    radiation_type: int = 0
    field_of_view: float = 0.0
    min_range: float = 0.0
    max_range: float = 0.0
    range: float = 0.0
    variance: float = 0.0

    ULTRASOUND: ClassVar[int] = 0
    INFRARED: ClassVar[int] = 1

    __msgtype__: ClassVar[str] = "sensor_msgs/msg/Range"


__all__ = ["Range"]