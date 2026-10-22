# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Format:
    pixel_format: str = ""
    width: int = 0
    height: int = 0
    fps: float = 0.0


    __msgtype__: ClassVar[str] = "usb_cam/msg/Format"


__all__ = ["Format"]