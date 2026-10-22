# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.duration import Duration


@dataclass(slots=True)
class QoSProfile:
    depth: int = 0
    deadline: Duration = field(default_factory=Duration)
    lifespan: Duration = field(default_factory=Duration)
    history: int = 0
    reliability: int = 0
    durability: int = 0
    liveliness: int = 0
    liveliness_lease_duration: Duration = field(default_factory=Duration)

    HISTORY_SYSTEM_DEFAULT: ClassVar[int] = 0
    HISTORY_KEEP_LAST: ClassVar[int] = 1
    HISTORY_KEEP_ALL: ClassVar[int] = 2
    HISTORY_UNKNOWN: ClassVar[int] = 3
    RELIABILITY_SYSTEM_DEFAULT: ClassVar[int] = 0
    RELIABILITY_RELIABLE: ClassVar[int] = 1
    RELIABILITY_BEST_EFFORT: ClassVar[int] = 2
    RELIABILITY_UNKNOWN: ClassVar[int] = 3
    RELIABILITY_BEST_AVAILABLE: ClassVar[int] = 4
    DURABILITY_SYSTEM_DEFAULT: ClassVar[int] = 0
    DURABILITY_TRANSIENT_LOCAL: ClassVar[int] = 1
    DURABILITY_VOLATILE: ClassVar[int] = 2
    DURABILITY_UNKNOWN: ClassVar[int] = 3
    DURABILITY_BEST_AVAILABLE: ClassVar[int] = 4
    LIVELINESS_SYSTEM_DEFAULT: ClassVar[int] = 0
    LIVELINESS_AUTOMATIC: ClassVar[int] = 1
    LIVELINESS_MANUAL_BY_TOPIC: ClassVar[int] = 3
    LIVELINESS_UNKNOWN: ClassVar[int] = 4
    LIVELINESS_BEST_AVAILABLE: ClassVar[int] = 5

    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/QoSProfile"


__all__ = ["QoSProfile"]