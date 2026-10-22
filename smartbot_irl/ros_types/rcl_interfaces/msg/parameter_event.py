# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time
from .parameter import Parameter


@dataclass(slots=True)
class ParameterEvent:
    stamp: Time = field(default_factory=Time)
    node: str = ""
    new_parameters: list[Parameter] = field(default_factory=list)
    changed_parameters: list[Parameter] = field(default_factory=list)
    deleted_parameters: list[Parameter] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/ParameterEvent"


__all__ = ["ParameterEvent"]