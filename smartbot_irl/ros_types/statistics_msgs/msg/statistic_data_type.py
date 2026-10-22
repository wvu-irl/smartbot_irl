# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class StatisticDataType:
    pass

    STATISTICS_DATA_TYPE_UNINITIALIZED: ClassVar[int] = 0
    STATISTICS_DATA_TYPE_AVERAGE: ClassVar[int] = 1
    STATISTICS_DATA_TYPE_MINIMUM: ClassVar[int] = 2
    STATISTICS_DATA_TYPE_MAXIMUM: ClassVar[int] = 3
    STATISTICS_DATA_TYPE_STDDEV: ClassVar[int] = 4
    STATISTICS_DATA_TYPE_SAMPLE_COUNT: ClassVar[int] = 5

    __msgtype__: ClassVar[str] = "statistics_msgs/msg/StatisticDataType"


__all__ = ["StatisticDataType"]