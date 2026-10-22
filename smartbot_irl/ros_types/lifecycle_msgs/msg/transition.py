# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Transition:
    id: int = 0
    label: str = ""

    TRANSITION_CREATE: ClassVar[int] = 0
    TRANSITION_CONFIGURE: ClassVar[int] = 1
    TRANSITION_CLEANUP: ClassVar[int] = 2
    TRANSITION_ACTIVATE: ClassVar[int] = 3
    TRANSITION_DEACTIVATE: ClassVar[int] = 4
    TRANSITION_UNCONFIGURED_SHUTDOWN: ClassVar[int] = 5
    TRANSITION_INACTIVE_SHUTDOWN: ClassVar[int] = 6
    TRANSITION_ACTIVE_SHUTDOWN: ClassVar[int] = 7
    TRANSITION_DESTROY: ClassVar[int] = 8
    TRANSITION_ON_CONFIGURE_SUCCESS: ClassVar[int] = 10
    TRANSITION_ON_CONFIGURE_FAILURE: ClassVar[int] = 11
    TRANSITION_ON_CONFIGURE_ERROR: ClassVar[int] = 12
    TRANSITION_ON_CLEANUP_SUCCESS: ClassVar[int] = 20
    TRANSITION_ON_CLEANUP_FAILURE: ClassVar[int] = 21
    TRANSITION_ON_CLEANUP_ERROR: ClassVar[int] = 22
    TRANSITION_ON_ACTIVATE_SUCCESS: ClassVar[int] = 30
    TRANSITION_ON_ACTIVATE_FAILURE: ClassVar[int] = 31
    TRANSITION_ON_ACTIVATE_ERROR: ClassVar[int] = 32
    TRANSITION_ON_DEACTIVATE_SUCCESS: ClassVar[int] = 40
    TRANSITION_ON_DEACTIVATE_FAILURE: ClassVar[int] = 41
    TRANSITION_ON_DEACTIVATE_ERROR: ClassVar[int] = 42
    TRANSITION_ON_SHUTDOWN_SUCCESS: ClassVar[int] = 50
    TRANSITION_ON_SHUTDOWN_FAILURE: ClassVar[int] = 51
    TRANSITION_ON_SHUTDOWN_ERROR: ClassVar[int] = 52
    TRANSITION_ON_ERROR_SUCCESS: ClassVar[int] = 60
    TRANSITION_ON_ERROR_FAILURE: ClassVar[int] = 61
    TRANSITION_ON_ERROR_ERROR: ClassVar[int] = 62
    TRANSITION_CALLBACK_SUCCESS: ClassVar[int] = 97
    TRANSITION_CALLBACK_FAILURE: ClassVar[int] = 98
    TRANSITION_CALLBACK_ERROR: ClassVar[int] = 99

    __msgtype__: ClassVar[str] = "lifecycle_msgs/msg/Transition"


__all__ = ["Transition"]