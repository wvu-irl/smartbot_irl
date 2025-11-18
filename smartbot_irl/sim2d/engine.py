# engine.py
import math
from math import cos, sin
import time
from dataclasses import dataclass
from ..data import Command, SensorData


class SimEngine:
    """Simple 2D differential-drive sim.

    Returns:
        _type_: _description_
    """

    def __init__(self, wheel_base: float = 0.3):
        self.wheel_base = wheel_base
        # self.last_t = time.time()
        self.state = SensorData.initialized()  # holds all simulated values
        self._last_vx = 0.0
        self._last_vy = 0.0
        self.vx_body = 0.0
        self.prev_vx_body = 0.0

        self.obstacles: list[tuple[float, float, float, float]] = []

        # simple map: square arena, meters
        self.arena = {
            'xmin': -5.0,
            'xmax': 5.0,
            'ymin': -5.0,
            'ymax': 5.0,
        }

        self.markers: list[tuple[float, float]] = [(2.0, 2.0)]  # initial marker(s)

    # ------------------------------------------------------------------
    def apply_command(self, cmd: Command) -> None:
        """Apply a Command instance to the simulated robot.

        Wheel velocity is treated as a perfect instant command.

        Args:
            cmd (Command): _description_
        """
        s = self.state

        lin = cmd.linear_vel or 0.0
        ang = cmd.angular_vel or 0.0
        wl = cmd.wheel_vel_left or 0.0
        wr = cmd.wheel_vel_right or 0.0

        if cmd.linear_vel is not None or cmd.angular_vel is not None:
            # Twist commands are in body frame.
            wl = lin - 0.5 * self.wheel_base * ang
            wr = lin + 0.5 * self.wheel_base * ang

        s.joints.velocities[0] = wl
        s.joints.velocities[1] = wr

        # Zero-slip differential drive kinematic model (body frame).
        # self.vx_body = (wl + wr) / 2.0

        # # Put in odom frame.
        # s.odom.vx = cos(s.odom.yaw) * self.vx_body
        # s.odom.vy = sin(s.odom.yaw) * self.vx_body

        # # Already in odom frame?
        # s.odom.wz = (wr - wl) / self.wheel_base

        s.manipulator_curr_preset = cmd.manipulator_presets

        if cmd.gripper_closed:
            s.gripper_curr_state = 'CLOSED'
        else:
            s.gripper_curr_state = 'OPEN'

    # ------------------------------------------------------------------
    def step(self, dt: float) -> SensorData:
        """Integrate robot motion forward by dt and return updated SensorData.

        Args:
            dt (float | None, optional): _description_. Defaults to None.

        Returns:
            SensorData: _description_
        """
        # now = time.time()
        # if dt is None:
        #     dt = now - self.last_t
        # self.last_t = now

        s = self.state
        wl = s.joints.velocities[0]
        wr = s.joints.velocities[1]

        # Zero-slip differential drive kinematic model (body frame).
        self.prev_vx_body = self.vx_body
        ideal_vel = (wl + wr) / 2.0

        # first-order dynamics
        alpha = dt / (0.2 + dt)
        self.prev_vx_body = self.vx_body
        self.vx_body = (1 - alpha) * self.vx_body + alpha * ideal_vel

        # Put lin vel in odom frame.
        s.odom.vx = cos(s.odom.yaw) * self.vx_body
        s.odom.vy = sin(s.odom.yaw) * self.vx_body

        # Ang vel in odom frame.
        s.odom.wz = (wr - wl) / self.wheel_base

        # Integrate pose (odom frame).
        # Odom is perfect true simulator pos.
        s.odom.yaw += s.odom.wz * dt
        s.odom.x += s.odom.vx * dt
        s.odom.y += s.odom.vy * dt

        # Update wheel positions
        # s.joints.positions += s.joints.velocities * dt
        s.joints.positions = [p + v * dt for p, v in zip(s.joints.positions, s.joints.velocities)]

        if s.odom.yaw > math.pi:
            s.odom.yaw -= 2 * math.pi
        elif s.odom.yaw < -math.pi:
            s.odom.yaw += 2 * math.pi

        # Update synthetic sensor readings
        self._update_lidar()
        self._update_markers()
        self._update_imu(dt)

        return s

    def add_obstacle(self, x: float, y: float, w: float, h: float) -> None:
        """Add an axis-aligned rectangular obstacle centered at (x, y).

        Args:
            x (float): _description_
            y (float): _description_
            w (float): _description_
            h (float): _description_
        """

        half_w, half_h = w / 2.0, h / 2.0
        self.obstacles.append((x - half_w, x + half_w, y - half_h, y + half_h))

    def _update_imu(
        self,
        dt: float,
    ):
        s = self.state

        # angular velocity (gyroscope). Yoink from odom (true state).
        gyro_z = s.odom.wz

        # Just use our simulator's vx from wheel vels.
        ax = (self.vx_body - self.prev_vx_body) / dt if dt > 1e-6 else 0.0

        # centripetal ay.
        ay = self.vx_body * s.odom.wz  # centripetal accel

        # add a bit of sensor noise
        import random

        noise = lambda s: s + random.gauss(0, 0.02)

        s.imu.wz = noise(gyro_z)
        s.imu.ax = noise(ax)
        s.imu.ay = noise(ay)

    def _update_lidar(self):
        """Populate self.state.scan with simulated range readings."""
        s = self.state
        scan = s.scan
        N = len(scan.ranges)
        x, y, theta = s.odom.x, s.odom.y, s.odom.yaw

        max_range = 4.0  # meters
        step = 0.05  # meters per step along ray

        for i in range(N):
            angle = theta + scan.angle_min + i * scan.angle_increment
            r = 0.0
            while r < max_range:
                rx = x + r * math.cos(angle)
                ry = y + r * math.sin(angle)
                if (
                    rx <= self.arena['xmin']
                    or rx >= self.arena['xmax']
                    or ry <= self.arena['ymin']
                    or ry >= self.arena['ymax']
                ):
                    break
                # Check obstacles
                hit = False
                for xmin, xmax, ymin, ymax in self.obstacles:
                    if xmin <= rx <= xmax and ymin <= ry <= ymax:
                        hit = True
                        break
                if hit:
                    break
                r += step
            scan.ranges[i] = min(r, max_range)

    def place_hex(self, x: float | None = None, y: float | None = None):
        """Place a new simulated marker in the world at (x, y) or a random obstacle-free location.

        Args:
            x (float | None, optional): _description_. Defaults to None.
            y (float | None, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        import random

        def is_inside_obstacle(px: float, py: float, margin: float = 1) -> bool:
            """Check whether (px, py) is inside or too close to any obstacle."""
            for xmin, xmax, ymin, ymax in self.obstacles:
                if (xmin - margin) <= px <= (xmax + margin) and (ymin - margin) <= py <= (
                    ymax + margin
                ):
                    return True
            return False

        def is_near_wall(px: float, py: float, wall_margin: float = 1) -> bool:
            """Check whether (px, py) is too close to the arena walls."""
            return (
                (px - self.arena['xmin']) < wall_margin
                or (self.arena['xmax'] - px) < wall_margin
                or (py - self.arena['ymin']) < wall_margin
                or (self.arena['ymax'] - py) < wall_margin
            )

        # Robot position, used to avoid spawning too close
        rx, ry = self.state.odom.x, self.state.odom.y

        if x is not None and y is not None:
            if is_inside_obstacle(x, y):
                print(
                    f'[WARN] Tried to place marker inside obstacle at ({x:.2f}, {y:.2f}), ignored.'
                )
                return
            if is_near_wall(x, y):
                print(
                    f'[WARN] Tried to place marker too close to wall at ({x:.2f}, {y:.2f}), ignored.'
                )
                return
            self.markers = [(x, y)]
            return

        # --- Random placement with obstacle rejection ---
        max_attempts = 50
        buffer = 0.3
        for attempt in range(max_attempts):
            x = random.uniform(self.arena['xmin'] + buffer, self.arena['xmax'] - buffer)
            y = random.uniform(self.arena['ymin'] + buffer, self.arena['ymax'] - buffer)

            too_close_to_robot = math.hypot(x - rx, y - ry) < 0.5
            if is_inside_obstacle(x, y) or is_near_wall(x, y) or too_close_to_robot:
                continue

            # Valid spot
            self.markers = [(x, y)]
            print(f'Placed hex at ({x:.2f}, {y:.2f}) after {attempt + 1} attempts')
            return

        print('[WARN] Failed to find obstacle-free location for marker after many attempts.')

    def _update_markers(self):
        """Compute marker poses relative to the robot body frame."""
        from ..data import Pose, PoseArray, ArucoMarkers

        s = self.state
        rx, ry, rtheta = s.odom.x, s.odom.y, s.odom.yaw

        rel_poses = []
        for mx, my in self.markers:
            dx = mx - rx
            dy = my - ry
            # Transform from world to robot frame
            rel_x = math.cos(-rtheta) * dx - math.sin(-rtheta) * dy
            rel_y = math.sin(-rtheta) * dx + math.cos(-rtheta) * dy
            rel_poses.append(Pose(x=rel_x, y=rel_y, z=0.0))
        s.seen_hexes = ArucoMarkers(poses=rel_poses, marker_ids=[48] * len(rel_poses))

    def read_all(self):
        return self.state

    def reset(self):
        self.state = SensorData()
        # self.last_t = time.time()
