# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class KeyValue:
    key: str = ""
    value: str = ""


    __msgtype__: ClassVar[str] = "diagnostic_msgs/msg/KeyValue"


__all__ = ["KeyValue"]