# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .interface_type import InterfaceType
from .qo_s_profile import QoSProfile


@dataclass(slots=True)
class Service:
    name: str = ""
    request_type: InterfaceType = field(default_factory=InterfaceType)
    request_qos: QoSProfile = field(default_factory=QoSProfile)
    response_type: InterfaceType = field(default_factory=InterfaceType)
    response_qos: QoSProfile = field(default_factory=QoSProfile)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/Service"


__all__ = ["Service"]