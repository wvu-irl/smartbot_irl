# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .key_value import KeyValue


@dataclass(slots=True)
class DiagnosticStatus:
    level: bytes = bytes([0])
    name: str = ""
    message: str = ""
    hardware_id: str = ""
    values: list[KeyValue] = field(default_factory=list)

    OK: ClassVar[bytes] = b'\x00'
    WARN: ClassVar[bytes] = b'\x01'
    ERROR: ClassVar[bytes] = b'\x02'
    STALE: ClassVar[bytes] = b'\x03'

    __msgtype__: ClassVar[str] = "diagnostic_msgs/msg/DiagnosticStatus"


__all__ = ["DiagnosticStatus"]