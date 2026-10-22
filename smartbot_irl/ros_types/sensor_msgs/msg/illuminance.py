# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Illuminance:
    header: Header = field(default_factory=Header)
    illuminance: float = 0.0
    variance: float = 0.0


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/Illuminance"


__all__ = ["Illuminance"]