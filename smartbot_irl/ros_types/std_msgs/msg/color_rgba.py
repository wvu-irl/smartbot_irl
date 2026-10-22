# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class ColorRGBA:
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 0.0


    __msgtype__: ClassVar[str] = "std_msgs/msg/ColorRGBA"


__all__ = ["ColorRGBA"]