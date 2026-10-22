# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .interface_type import InterfaceType
from .qo_s_profile import QoSProfile


@dataclass(slots=True)
class Topic:
    name: str = ""
    type: InterfaceType = field(default_factory=InterfaceType)
    qos: QoSProfile = field(default_factory=QoSProfile)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/Topic"


__all__ = ["Topic"]