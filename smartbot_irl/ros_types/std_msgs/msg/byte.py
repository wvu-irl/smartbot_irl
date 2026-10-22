# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Byte:
    data: bytes = bytes([0])


    __msgtype__: ClassVar[str] = "std_msgs/msg/Byte"


__all__ = ["Byte"]