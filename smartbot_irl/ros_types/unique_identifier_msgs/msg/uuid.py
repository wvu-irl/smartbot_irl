# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class UUID:
    uuid: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.zeros(16, dtype=numpy.uint8))


    __msgtype__: ClassVar[str] = "unique_identifier_msgs/msg/UUID"


__all__ = ["UUID"]