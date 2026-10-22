# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time


@dataclass(slots=True)
class Clock:
    clock: Time = field(default_factory=Time)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/Clock"


__all__ = ["Clock"]