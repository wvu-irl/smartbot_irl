from dataclasses import dataclass, field
import numpy as np


class Component:
    """Generic Component"""

    def update(self, world, dt):
        raise NotImplementedError


@dataclass
class DiffDriveWheels(Component):
    """State of the robots two wheels"""

    w_l: float = 0.0
    w_r: float = 0.0
    theta_l: float = 0.0
    theta_r: float = 0.0
    wheel_radius: float = 1.0
    wheel_base: float = 0.3


@dataclass
class Body(Component):
    """Generic circle object"""

    mass: float = 0.0  # Does nothing for now.
    pos_x: float = 0.0
    pos_y: float = 0.0
    theta: float = 0.0
    vel_x: float = 0.0
    vel_y: float = 0.0
    wz: float = 0.0
    radius: float = 0.3


@dataclass
class IMU(Component):
    """Corrupted versions of true body linear accel + ang vel."""

    ax: float = 0.0
    ay: float = 0.0
    wz: float = 0.0


@dataclass
class Lidar(Component):
    """Simple lidar"""

    num_rays: int = 360
    start_angle: float = -np.pi
    end_angle: float = np.pi
    ranges: list[float] = field(default_factory=lambda: [5.0] * 360)


@dataclass
class DiffDriveWheelsEncoders(Component):
    """Corrupted versions of true wheel state."""

    w_l: float = 0.0
    w_r: float = 0.0
    theta_l: float = 0.0
    theta_r: float = 0.0
    wheel_radius: float = 0.0
    wheel_base: float = 0.0
