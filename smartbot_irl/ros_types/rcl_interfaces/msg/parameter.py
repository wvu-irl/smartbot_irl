# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .parameter_value import ParameterValue


@dataclass(slots=True)
class Parameter:
    name: str = ""
    value: ParameterValue = field(default_factory=ParameterValue)


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/Parameter"


__all__ = ["Parameter"]