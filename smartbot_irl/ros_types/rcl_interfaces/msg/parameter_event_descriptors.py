# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .parameter_descriptor import ParameterDescriptor


@dataclass(slots=True)
class ParameterEventDescriptors:
    new_parameters: list[ParameterDescriptor] = field(default_factory=list)
    changed_parameters: list[ParameterDescriptor] = field(default_factory=list)
    deleted_parameters: list[ParameterDescriptor] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/ParameterEventDescriptors"


__all__ = ["ParameterEventDescriptors"]