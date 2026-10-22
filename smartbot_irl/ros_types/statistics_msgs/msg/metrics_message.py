# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time
from .statistic_data_point import StatisticDataPoint


@dataclass(slots=True)
class MetricsMessage:
    measurement_source_name: str = ""
    metrics_source: str = ""
    unit: str = ""
    window_start: Time = field(default_factory=Time)
    window_stop: Time = field(default_factory=Time)
    statistics: list[StatisticDataPoint] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "statistics_msgs/msg/MetricsMessage"


__all__ = ["MetricsMessage"]