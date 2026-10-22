# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time


@dataclass(slots=True)
class Log:
    stamp: Time = field(default_factory=Time)
    level: int = 0
    name: str = ""
    msg: str = ""
    file: str = ""
    function: str = ""
    line: int = 0

    DEBUG: ClassVar[int] = 10
    INFO: ClassVar[int] = 20
    WARN: ClassVar[int] = 30
    ERROR: ClassVar[int] = 40
    FATAL: ClassVar[int] = 50

    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/Log"


__all__ = ["Log"]