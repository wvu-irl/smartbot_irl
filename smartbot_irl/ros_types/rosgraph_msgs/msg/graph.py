# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .node import Node


@dataclass(slots=True)
class Graph:
    nodes: list[Node] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rosgraph_msgs/msg/Graph"


__all__ = ["Graph"]