# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...rcl_interfaces.msg.parameter_descriptor import ParameterDescriptor
from ...rcl_interfaces.msg.parameter_value import ParameterValue
from .action import Action
from .service import Service
from .topic import Topic


@dataclass(slots=True)
class Node:
    name: str = ""
    parameters: list[ParameterDescriptor] = field(default_factory=list)
    parameter_values: list[ParameterValue] = field(default_factory=list)
    publishers: list[Topic] = field(default_factory=list)
    subscriptions: list[Topic] = field(default_factory=list)
    service_clients: list[Service] = field(default_factory=list)
    service_servers: list[Service] = field(default_factory=list)
    action_clients: list[Action] = field(default_factory=list)
    action_servers: list[Action] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/Node"


__all__ = ["Node"]