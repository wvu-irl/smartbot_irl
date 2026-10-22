# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...builtin_interfaces.msg.time import Time


@dataclass(slots=True)
class ServiceEventInfo:
    event_type: int = 0
    stamp: Time = field(default_factory=Time)
    client_gid: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.zeros(16, dtype=numpy.uint8))
    sequence_number: int = 0

    REQUEST_SENT: ClassVar[int] = 0
    REQUEST_RECEIVED: ClassVar[int] = 1
    RESPONSE_SENT: ClassVar[int] = 2
    RESPONSE_RECEIVED: ClassVar[int] = 3

    __msgtype__: ClassVar[str] = "service_msgs/msg/ServiceEventInfo"


__all__ = ["ServiceEventInfo"]