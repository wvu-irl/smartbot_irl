# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time


@dataclass(slots=True)
class Header:
    stamp: Time = field(default_factory=Time)
    frame_id: str = ""


    __msgtype__: ClassVar[str] = "std_msgs/msg/Header"


__all__ = ["Header"]