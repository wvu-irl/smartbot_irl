# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .diagnostic_status import DiagnosticStatus
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class DiagnosticArray:
    header: Header = field(default_factory=Header)
    status: list[DiagnosticStatus] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "diagnostic_msgs/msg/DiagnosticArray"


__all__ = ["DiagnosticArray"]