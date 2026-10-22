# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class StatisticDataPoint:
    data_type: int = 0
    data: float = 0.0


    __msgtype__: ClassVar[str] = "statistics_msgs/msg/StatisticDataPoint"


__all__ = ["StatisticDataPoint"]