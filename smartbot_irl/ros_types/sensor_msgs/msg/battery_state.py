# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class BatteryState:
    header: Header = field(default_factory=Header)
    voltage: float = 0.0
    temperature: float = 0.0
    current: float = 0.0
    charge: float = 0.0
    capacity: float = 0.0
    design_capacity: float = 0.0
    percentage: float = 0.0
    power_supply_status: int = 0
    power_supply_health: int = 0
    power_supply_technology: int = 0
    present: bool = False
    cell_voltage: NDArray[numpy.float32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float32))
    cell_temperature: NDArray[numpy.float32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float32))
    location: str = ""
    serial_number: str = ""

    POWER_SUPPLY_STATUS_UNKNOWN: ClassVar[int] = 0
    POWER_SUPPLY_STATUS_CHARGING: ClassVar[int] = 1
    POWER_SUPPLY_STATUS_DISCHARGING: ClassVar[int] = 2
    POWER_SUPPLY_STATUS_NOT_CHARGING: ClassVar[int] = 3
    POWER_SUPPLY_STATUS_FULL: ClassVar[int] = 4
    POWER_SUPPLY_HEALTH_UNKNOWN: ClassVar[int] = 0
    POWER_SUPPLY_HEALTH_GOOD: ClassVar[int] = 1
    POWER_SUPPLY_HEALTH_OVERHEAT: ClassVar[int] = 2
    POWER_SUPPLY_HEALTH_DEAD: ClassVar[int] = 3
    POWER_SUPPLY_HEALTH_OVERVOLTAGE: ClassVar[int] = 4
    POWER_SUPPLY_HEALTH_UNSPEC_FAILURE: ClassVar[int] = 5
    POWER_SUPPLY_HEALTH_COLD: ClassVar[int] = 6
    POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE: ClassVar[int] = 7
    POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE: ClassVar[int] = 8
    POWER_SUPPLY_TECHNOLOGY_UNKNOWN: ClassVar[int] = 0
    POWER_SUPPLY_TECHNOLOGY_NIMH: ClassVar[int] = 1
    POWER_SUPPLY_TECHNOLOGY_LION: ClassVar[int] = 2
    POWER_SUPPLY_TECHNOLOGY_LIPO: ClassVar[int] = 3
    POWER_SUPPLY_TECHNOLOGY_LIFE: ClassVar[int] = 4
    POWER_SUPPLY_TECHNOLOGY_NICD: ClassVar[int] = 5
    POWER_SUPPLY_TECHNOLOGY_LIMN: ClassVar[int] = 6
    POWER_SUPPLY_TECHNOLOGY_TERNARY: ClassVar[int] = 7
    POWER_SUPPLY_TECHNOLOGY_VRLA: ClassVar[int] = 8

    __msgtype__: ClassVar[str] = "sensor_msgs/msg/BatteryState"


__all__ = ["BatteryState"]