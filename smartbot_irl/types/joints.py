from __future__ import annotations

from dataclasses import dataclass, field
from math import nan

from smartbot_irl.ros_types.sensor_msgs.msg import JointState as RosJointState

from .base_type import BaseType


@dataclass
class Joints(BaseType):
    names: list[str] = field(default_factory=list)
    positions: list[float] = field(default_factory=list)
    velocities: list[float] = field(default_factory=list)

    stamp_sec: int = 0
    stamp_nanosec: int = 0

    @classmethod
    def from_ros(cls, msg: RosJointState) -> Joints:
        return cls(
            names=list(msg.name),
            positions=list(msg.position),
            velocities=list(msg.velocity),
            stamp_sec=msg.header.stamp.sec,
            stamp_nanosec=msg.header.stamp.nanosec,
        )

    def to_ros(self): ...

    def _joint_value(self, name: str, values: list[float]) -> float:
        try:
            index = self.names.index(name)
        except ValueError:
            return nan

        if index >= len(values):
            return nan

        return values[index]

    @property
    def left_pos(self) -> float:
        return self._joint_value('LDrive', self.positions)

    @property
    def right_pos(self) -> float:
        return self._joint_value('RDrive', self.positions)

    @property
    def left_vel(self) -> float:
        return self._joint_value('LDrive', self.velocities)

    @property
    def right_vel(self) -> float:
        return self._joint_value('RDrive', self.velocities)

    # @property
    # def left_pos(self) -> float:
    #     return self.positions[self.names.index('LDrive')]

    # @property
    # def right_pos(self) -> float:
    #     return self.positions[self.names.index('RDrive')]

    # @property
    # def left_vel(self) -> float:
    #     return self.velocities[self.names.index('LDrive')]

    # @property
    # def right_vel(self) -> float:
    #     return self.velocities[self.names.index('RDrive')]
