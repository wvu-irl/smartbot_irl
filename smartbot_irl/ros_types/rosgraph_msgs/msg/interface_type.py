# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .type_hash import TypeHash


@dataclass(slots=True)
class InterfaceType:
    name: str = ""
    hash: TypeHash = field(default_factory=TypeHash)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/InterfaceType"


__all__ = ["InterfaceType"]