from queue import Empty

from ..data import SensorData, Command
from ._components import IMU, Body, DiffDriveWheels, DiffDriveWheelsEncoders
import numpy as np
from ..utils.smart_logging import SmartLogger, logging

logger = SmartLogger(level=logging.DEBUG)  # Print statements, but better!


class System:
    """Generic System"""

    def update(self, world, dt):
        raise NotImplementedError


class DiffDriveKinematics(System):
    components = (Body, DiffDriveWheels)

    def update(self, body: Body, wheels: DiffDriveWheels, dt):
        v_l = wheels.wheel_radius * wheels.w_l
        v_r = wheels.wheel_radius * wheels.w_r

        v = 0.5 * (v_l + v_r)
        omega = (v_r - v_l) / wheels.wheel_base

        body.vel_x = v * np.cos(body.theta)
        body.vel_y = v * np.sin(body.theta)
        body.wz = omega


class EncoderSystem(System):
    components = (DiffDriveWheels, DiffDriveWheelsEncoders)

    def update(self, wheels, enc, dt):
        enc.w_l = wheels.w_l + 0.00 * np.random.randn()
        enc.w_r = wheels.w_r + 0.00 * np.random.randn()
        enc.theta_l += enc.w_l * dt
        enc.theta_r += enc.w_r * dt


class Integrate(System):
    components = (Body,)

    def update(self, body, dt) -> None:
        body.pos_x += body.vel_x * dt
        body.pos_y += body.vel_y * dt
        body.theta += body.wz * dt


class DetectCollision(System):
    """Check if object is inside another. Assume circles."""

    components = (Body,)

    def update(self, body, dt): ...


class GetInput:
    """Accept Command object"""

    components = (DiffDriveWheels,)

    def __init__(self, cmd_queue) -> None:
        self.cmd_queue = cmd_queue

    def update(self, wheels, dt) -> None:
        try:
            logger.debug(f'command_queue: {cmd}', rate=5)
            cmd: Command = self.cmd_queue.get_nowait()  # will return None if empty
        except Empty:
            return

        wheels.w_l = cmd.wheel_vel_left
        wheels.w_r = cmd.wheel_vel_right


class Read:
    """Packages sim sensor data and sends to an external output queue."""

    components = (Body, DiffDriveWheels, IMU)

    def __init__(self, world, out_queue, publish_rate_hz=10.0) -> None:
        self.out_queue = out_queue
        self.period = 1.0 / publish_rate_hz
        self.next_pub_time = 0.0
        self.world = world

    def update(self, body: Body, wheels: DiffDriveWheels, imu: IMU, dt: float) -> None:
        """Returns a SensorData object from simulation.

        Parameters
        ----------
        body : Body
            _description_
        wheels : DiffDriveWheels
            _description_
        imu : IMU
            _description_
        dt : float
            _description_
        """
        # logger.info(f'Sensordata in read is')

        # Only publish at desired rate
        if self.world.time < self.next_pub_time:
            return
        self.next_pub_time = self.world.time + self.period

        # TODO Completely fill out sensordata.
        sensor_data = SensorData()
        sensor_data.odom.x = body.pos_x
        sensor_data.odom.y = body.pos_y
        sensor_data.odom.yaw = body.theta

        # msg = {
        #     'time': self.world.time,
        #     'pose': {
        #         'x': body.pos_x,
        #         'y': body.pos_y,
        #         'theta': body.theta,
        #     },
        #     'twist': {
        #         'vx': body.vel_x,
        #         'vy': body.vel_y,
        #         'wz': body.wz,
        #     },
        #     'wheels': {
        #         'w_l': wheels.w_l,
        #         'w_r': wheels.w_r,
        #     },
        #     'imu': {
        #         'ax': imu.ax,
        #         'ay': imu.ay,
        #         'wz': imu.wz,
        #     },
        # }
        self.out_queue.put(sensor_data)


class DebugPrint:
    components = (Body,)

    def update(self, body, dt) -> None:
        print(
            f'[Body] x={body.pos_x:.2f}  y={body.pos_y:.2f}  '
            f'theta={body.theta:.2f}  vx={body.vel_x:.2f}  vy={body.vel_y:.2f}'
        )
