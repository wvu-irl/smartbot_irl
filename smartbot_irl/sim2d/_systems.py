from queue import Empty

import smartbot_irl.data as data

# from ..data import (
#     SensorData,
#     Command,
#     IMU,
#     Bool,
#     JointState,
#     LaserScan,
#     Pose,
#     PoseArray,
#     ArucoMarkers,
#     String,
#     Odometry,
# )
from ._components import IMU, Body, DiffDriveWheels, DiffDriveWheelsEncoders, Lidar
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
            cmd: data.Command = self.cmd_queue.get_nowait()  # will return None if empty
            logger.debug(f'command_queue: {cmd.linear_vel}', rate=5)

        except Empty:
            return

        # Do kinematics.
        v = cmd.linear_vel
        w = cmd.angular_vel
        r = 0.125
        L = 0.3

        # v = (r/2) * (wl + wr)
        # w = (r/L) * (wr - wl)
        w_l = (v - 0.5 * L * w) / r
        w_r = (v + 0.5 * L * w) / r

        wheels.w_l = w_l
        wheels.w_r = w_r

        # Only if we want to make wheel vels directly the command
        # wheels.w_l = cmd.wheel_vel_left
        # wheels.w_r = cmd.wheel_vel_right


class Read:
    """Packages sim sensor data and sends to an external output queue."""

    components = (Body, DiffDriveWheels, IMU, Lidar)

    def __init__(self, world, out_queue, publish_rate_hz=10.0) -> None:
        self.out_queue = out_queue
        self.period = 1.0 / publish_rate_hz
        self.next_pub_time = 0.0
        self.world = world

    def update(
        self, body: Body, wheels: DiffDriveWheels, imu: IMU, lidar: Lidar, dt: float
    ) -> None:
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
        sensor_data = data.SensorData()
        sensor_data.odom.x = body.pos_x
        sensor_data.odom.y = body.pos_y
        sensor_data.odom.yaw = body.theta

        sensor_data.scan = data.LaserScan()
        sensor_data.scan.ranges = lidar.ranges
        sensor_data.scan.angle_increment = 0.05
        sensor_data.scan.angle_max = lidar.end_angle
        sensor_data.scan.angle_min = lidar.start_angle

        sensor_data.imu = data.IMU()

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


class LidarSystem(System):
    components = (Body, Lidar)

    def update(self, body: Body, lidar: Lidar, dt: float):
        #
        # Just output max ranges for now.

        angles = np.linspace(lidar.start_angle, lidar.end_angle, lidar.num_rays)
        ranges = np.ones_like(angles)

        x0 = body.pos_x
        y0 = body.pos_y
        yaw = body.theta

        for i, a in enumerate(angles):
            # Convert local beam angle -> world angle
            beam_angle = yaw + a

            # Ray direction
            dx = np.cos(beam_angle)
            dy = np.sin(beam_angle)

            # # March forward until hit or max distance
            # r = 0.0
            # step = 0.05  # resolution

            # hit_range = lidar.max_range

            # # Loop until out of range
            # while r < lidar.max_range:
            #     px = x0 + r * dx
            #     py = y0 + r * dy

            #     # Collision check
            #     for (xmin, xmax, ymin, ymax) in lidar.world.obstacles:
            #         if xmin <= px <= xmax and ymin <= py <= ymax:
            #             hit_range = r
            #             break

            #     if hit_range != lidar.max_range:
            #         break

            #     r += step

            # ranges[i] = hit_range

        lidar.ranges = 10 * ranges


class DebugPrint:
    components = (Body,)

    def update(self, body, dt) -> None:
        print(
            f'[Body] x={body.pos_x:.2f}  y={body.pos_y:.2f}  '
            f'theta={body.theta:.2f}  vx={body.vel_x:.2f}  vy={body.vel_y:.2f}'
        )
