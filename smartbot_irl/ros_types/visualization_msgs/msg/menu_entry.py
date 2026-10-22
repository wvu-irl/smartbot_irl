# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class MenuEntry:
    id: int = 0
    parent_id: int = 0
    title: str = ""
    command: str = ""
    command_type: int = 0

    FEEDBACK: ClassVar[int] = 0
    ROSRUN: ClassVar[int] = 1
    ROSLAUNCH: ClassVar[int] = 2

    __msgtype__: ClassVar[str] = "visualization_msgs/msg/MenuEntry"


__all__ = ["MenuEntry"]