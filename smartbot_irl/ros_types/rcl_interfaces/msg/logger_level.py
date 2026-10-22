# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class LoggerLevel:
    name: str = ""
    level: int = 0

    LOG_LEVEL_UNKNOWN: ClassVar[int] = 0
    LOG_LEVEL_DEBUG: ClassVar[int] = 10
    LOG_LEVEL_INFO: ClassVar[int] = 20
    LOG_LEVEL_WARN: ClassVar[int] = 30
    LOG_LEVEL_ERROR: ClassVar[int] = 40
    LOG_LEVEL_FATAL: ClassVar[int] = 50

    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/LoggerLevel"


__all__ = ["LoggerLevel"]