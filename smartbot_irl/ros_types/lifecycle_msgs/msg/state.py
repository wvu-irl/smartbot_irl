# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class State:
    id: int = 0
    label: str = ""

    PRIMARY_STATE_UNKNOWN: ClassVar[int] = 0
    PRIMARY_STATE_UNCONFIGURED: ClassVar[int] = 1
    PRIMARY_STATE_INACTIVE: ClassVar[int] = 2
    PRIMARY_STATE_ACTIVE: ClassVar[int] = 3
    PRIMARY_STATE_FINALIZED: ClassVar[int] = 4
    TRANSITION_STATE_CONFIGURING: ClassVar[int] = 10
    TRANSITION_STATE_CLEANINGUP: ClassVar[int] = 11
    TRANSITION_STATE_SHUTTINGDOWN: ClassVar[int] = 12
    TRANSITION_STATE_ACTIVATING: ClassVar[int] = 13
    TRANSITION_STATE_DEACTIVATING: ClassVar[int] = 14
    TRANSITION_STATE_ERRORPROCESSING: ClassVar[int] = 15

    __msgtype__: ClassVar[str] = "lifecycle_msgs/msg/State"


__all__ = ["State"]