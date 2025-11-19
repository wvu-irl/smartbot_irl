# engine.py
import math
from math import cos, sin
import time
from dataclasses import dataclass
from ..data import Command, SensorData
from ..data import Pose, PoseArray, ArucoMarkers
from .utils import make_arena

# from ..robot import SmartBotType
import random


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
        self.cam_fov = 70
        self.lidar_max_range = 10
        self.robot_radius = 0.2
        self.camera_range = 4

        self.obstacles: list[tuple[float, float, float, float]] = []

        # simple map: square arena, meters
        height = 8
        width = 8
        self.arena = {
            'xmin': -width,
            'xmax': width,
            'ymin': -height,
            'ymax': height,
        }
        self.add_obstacles(make_arena(width, height))

        self.markers: list[tuple[int, float, float]] = []
        self._next_marker_id = 0

    def _in_arena(self, x: float, y: float, margin: float = 0.0) -> bool:
        """Return True if (x,y) is inside arena bounds (with optional margin)."""
        return (
            self.arena['xmin'] + margin <= x <= self.arena['xmax'] - margin
            and self.arena['ymin'] + margin <= y <= self.arena['ymax'] - margin
        )

    def _would_collide(self, x: float, y: float) -> bool:
        """Return True if robot center at (x,y) would collide with arena or obstacles."""
        r = self.robot_radius
        # Outside arena => collision
        if not self._in_arena(x, y, margin=r):
            return True
        # Inside (inflated) obstacle => collision
        if self.is_inside_obstacle(x, y, margin=r):
            return True
        return False

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

        # # Put lin vel in odom frame.
        # s.odom.vx = cos(s.odom.yaw) * self.vx_body
        # s.odom.vy = sin(s.odom.yaw) * self.vx_body

        # Ang vel in odom frame.
        # s.odom.wz = (wr - wl) / self.wheel_base

        # # Integrate pose (odom frame).
        # # Odom is perfect true simulator pos.
        # s.odom.yaw += s.odom.wz * dt
        # s.odom.x += s.odom.vx * dt
        # s.odom.y += s.odom.vy * dt

        # Current pose
        x = s.odom.x
        y = s.odom.y
        yaw = s.odom.yaw

        # Velocities in odom frame
        s.odom.vx = cos(yaw) * self.vx_body
        s.odom.vy = sin(yaw) * self.vx_body
        s.odom.wz = (wr - wl) / self.wheel_base

        # Predict new pose
        x_new = x + s.odom.vx * dt
        y_new = y + s.odom.vy * dt
        yaw_new = yaw + s.odom.wz * dt

        # Normalize yaw_new into [-pi, pi]
        if yaw_new > math.pi:
            yaw_new -= 2 * math.pi
        elif yaw_new < -math.pi:
            yaw_new += 2 * math.pi

        # Collision check on the *translated* pose
        if self._would_collide(x_new, y_new):
            # Collision: do not move, zero linear velocity.
            # Allow rotation in place using yaw_new if you want rotation to continue,
            # or comment this line to stop rotation too.
            s.odom.x = x
            s.odom.y = y
            s.odom.yaw = yaw_new  # rotate in place on collision

            # Stop linear motion
            self.vx_body = 0.0
            s.odom.vx = 0.0
            s.odom.vy = 0.0
            s.joints.velocities[0] = 0.0
            s.joints.velocities[1] = 0.0
        else:
            # Free space: commit the move
            s.odom.x = x_new
            s.odom.y = y_new
            s.odom.yaw = yaw_new

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

    def add_obstacles(self, coords: list[float] | list[list[float]]) -> None:
        """Add one or more obstacles defined by two opposite corners.

        Parameters
        ----------
        coords : list[float] or list[list[float]]
            Either:
                [x1, y1, x2, y2]
            or:
                [[x1, y1, x2, y2], [...], ...]
        """

        # Normalize to a list of lists.
        if isinstance(coords[0], (int, float)):
            rects = [coords]  # single rectangle
        else:
            rects = coords  # list of rectangles
        rects: list  # TODO less stupid fix.

        for rect in rects:
            if len(rect) != 4:
                raise ValueError('Each obstacle must be a list of four floats: [x1, y1, x2, y2]')

            x1, y1, x2, y2 = rect

            xmin = min(x1, x2)
            xmax = max(x1, x2)
            ymin = min(y1, y2)
            ymax = max(y1, y2)

            self.obstacles.append((xmin, xmax, ymin, ymax))

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

        step = 0.01  # meters per step along ray
        noise = lambda s: s + random.gauss(0, 0.1)

        for i in range(N):
            angle = theta + scan.angle_min + i * scan.angle_increment
            r = 0.0
            while r < self.lidar_max_range:
                rx = x + r * math.cos(angle)
                ry = y + r * math.sin(angle)

                hit = False
                for xmin, xmax, ymin, ymax in self.obstacles:
                    if xmin <= rx <= xmax and ymin <= ry <= ymax:
                        hit = True
                        break
                if hit:
                    break
                r += noise(step)
            scan.ranges[i] = min(r, self.lidar_max_range)

    def is_inside_obstacle(self, px: float, py: float, margin: float = 1) -> bool:
        """Check whether (px, py) is inside or too close to any obstacle."""
        for xmin, xmax, ymin, ymax in self.obstacles:
            if (xmin - margin) <= px <= (xmax + margin) and (ymin - margin) <= py <= (
                ymax + margin
            ):
                return True
        return False

    def place_hex(self, x: float | None = None, y: float | None = None) -> None:
        """Place a new simulated marker in the world at (x, y) or a random obstacle-free location.

        Args:
            x (float | None, optional): _description_. Defaults to None.
            y (float | None, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        import random

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
            if self.is_inside_obstacle(x, y):
                print(
                    f'[WARN] Tried to place marker inside obstacle at ({x:.2f}, {y:.2f}), ignored.'
                )
                return
            if is_near_wall(x, y):
                print(
                    f'[WARN] Tried to place marker too close to wall at ({x:.2f}, {y:.2f}), ignored.'
                )
                return

            return

        # --- Random placement with obstacle rejection ---
        max_attempts = 50
        buffer = 0.3
        for attempt in range(max_attempts):
            x = random.uniform(self.arena['xmin'] + buffer, self.arena['xmax'] - buffer)
            y = random.uniform(self.arena['ymin'] + buffer, self.arena['ymax'] - buffer)

            too_close_to_robot = math.hypot(x - rx, y - ry) < 0.5
            if self.is_inside_obstacle(x, y) or is_near_wall(x, y) or too_close_to_robot:
                continue

            # Valid spot
            self._next_marker_id += 1
            self.markers.append((self._next_marker_id, x, y))

            print(f'Placed hex at ({x:.2f}, {y:.2f}) after {attempt + 1} attempts')
            return

        print('[WARN] Failed to find obstacle-free location for marker after many attempts.')

    def _update_markers(self):
        """Compute marker poses relative to the robot body frame.

        Use robots current pose and apply its cone of vision to get a list of
        see-able markers not behind an obstacle.
        """

        # Half-angle in radians
        half_fov = math.radians(self.cam_fov / 2)
        max_range = self.camera_range  # detection limit

        rel_poses = []
        rel_ids = []

        s = self.state
        rx, ry, rtheta = s.odom.x, s.odom.y, s.odom.yaw

        for mid, mx, my in self.markers:
            dx = mx - rx
            dy = my - ry
            # Transform from world to robot frame
            rel_x = math.cos(-rtheta) * dx - math.sin(-rtheta) * dy
            rel_y = math.sin(-rtheta) * dx + math.cos(-rtheta) * dy

            # Robot-frame polar coords
            ang = math.atan2(rel_y, rel_x)
            dist = math.hypot(rel_x, rel_y)

            # Reject behind or outside FOV
            if dist > max_range:
                continue
            if abs(ang) > half_fov:
                continue

            # Check if occluded.
            occluded = False
            steps = int(dist / 0.05)
            if steps < 1:
                steps = 1

            for i in range(1, steps):
                t = i / steps
                px = rx + t * dx
                py = ry + t * dy

                # Test against obstacles
                for xmin, xmax, ymin, ymax in self.obstacles:
                    if xmin <= px <= xmax and ymin <= py <= ymax:
                        occluded = True
                        break

                if occluded:
                    break

            if occluded:
                continue

            rel_poses.append(Pose(x=rel_x, y=rel_y, z=0.0))
            rel_ids.append(mid)
        s.seen_hexes = ArucoMarkers(poses=rel_poses, marker_ids=rel_ids)

    def read_all(self):
        return self.state

    def reset(self):
        self.state = SensorData()
        # self.last_t = time.time()
