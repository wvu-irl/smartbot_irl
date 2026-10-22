# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .multi_array_layout import MultiArrayLayout


@dataclass(slots=True)
class ByteMultiArray:
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: list[bytes] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "std_msgs/msg/ByteMultiArray"


__all__ = ["ByteMultiArray"]