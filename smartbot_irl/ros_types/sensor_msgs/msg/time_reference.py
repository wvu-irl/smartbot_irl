# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class TimeReference:
    header: Header = field(default_factory=Header)
    time_ref: Time = field(default_factory=Time)
    source: str = ""


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/TimeReference"


__all__ = ["TimeReference"]