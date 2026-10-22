# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class NavSatStatus:
    status: int = -2
    service: int = 0

    STATUS_UNKNOWN: ClassVar[int] = -2
    STATUS_NO_FIX: ClassVar[int] = -1
    STATUS_FIX: ClassVar[int] = 0
    STATUS_SBAS_FIX: ClassVar[int] = 1
    STATUS_GBAS_FIX: ClassVar[int] = 2
    SERVICE_UNKNOWN: ClassVar[int] = 0
    SERVICE_GPS: ClassVar[int] = 1
    SERVICE_GLONASS: ClassVar[int] = 2
    SERVICE_COMPASS: ClassVar[int] = 4
    SERVICE_GALILEO: ClassVar[int] = 8

    __msgtype__: ClassVar[str] = "sensor_msgs/msg/NavSatStatus"


__all__ = ["NavSatStatus"]