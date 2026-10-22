# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.duration import Duration
from ...builtin_interfaces.msg.time import Time


@dataclass(slots=True)
class Builtins:
    duration_value: Duration = field(default_factory=Duration)
    time_value: Time = field(default_factory=Time)


    __msgtype__: ClassVar[str] = "test_msgs/msg/Builtins"


__all__ = ["Builtins"]