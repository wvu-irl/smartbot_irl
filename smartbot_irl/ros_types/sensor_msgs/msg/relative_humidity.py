# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class RelativeHumidity:
    header: Header = field(default_factory=Header)
    relative_humidity: float = 0.0
    variance: float = 0.0


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/RelativeHumidity"


__all__ = ["RelativeHumidity"]