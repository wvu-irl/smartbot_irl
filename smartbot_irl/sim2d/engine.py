# engine.py
import math
import time
from dataclasses import dataclass
from ..data import Command, SensorData


class SimEngine:
    """
    Simple 2D differential-drive dynamics integrator.
    Integrates wheel velocities to pose using forward Euler.
    """

    def __init__(self, wheel_base: float = 0.3):
        self.wheel_base = wheel_base
        self.last_t = time.time()
        self.state = SensorData.initialized()  # holds all simulated values

        self.obstacles: list[tuple[float, float, float, float]] = []

        # simple map: square arena, meters
        self.arena = {
            "xmin": -5.0,
            "xmax": 5.0,
            "ymin": -5.0,
            "ymax": 5.0,
        }

        self.markers: list[tuple[float, float]] = [(2.0, 2.0)]  # initial marker(s)

    # ------------------------------------------------------------------
    def apply_command(self, cmd: Command) -> None:
        """Apply a Command instance to the simulated robot."""
        s = self.state

        lin = cmd.linear_vel or 0.0
        ang = cmd.angular_vel or 0.0
        wl = cmd.wheel_vel_left or 0.0
        wr = cmd.wheel_vel_right or 0.0

        if cmd.linear_vel is not None or cmd.angular_vel is not None:
            wl = lin - 0.5 * self.wheel_base * ang
            wr = lin + 0.5 * self.wheel_base * ang

        s.joints.velocities[0] = wl
        s.joints.velocities[1] = wr

        s.odom.vx = (wl + wr) / 2.0
        s.odom.wz = (wr - wl) / self.wheel_base
        s.manipulator_curr_preset = cmd.manipulator_presets

        if cmd.gripper_closed:
            s.gripper_curr_state = "CLOSED"
        else:
            s.gripper_curr_state = "OPEN"

    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> SensorData:
        """Integrate robot motion forward by dt and return updated SensorData."""
        now = time.time()
        if dt is None:
            dt = now - self.last_t
        self.last_t = now

        s = self.state

        # Integrate pose
        s.odom.yaw += s.odom.wz * dt
        s.odom.x += s.odom.vx * math.cos(s.odom.yaw) * dt
        s.odom.y += s.odom.vx * math.sin(s.odom.yaw) * dt

        if s.odom.yaw > math.pi:
            s.odom.yaw -= 2 * math.pi
        elif s.odom.yaw < -math.pi:
            s.odom.yaw += 2 * math.pi
        # Update synthetic sensor readings
        self._update_lidar()
        self._update_markers()

        return s

    def add_obstacle(self, x: float, y: float, w: float, h: float):
        """Add an axis-aligned rectangular obstacle centered at (x, y)."""
        half_w, half_h = w / 2.0, h / 2.0
        self.obstacles.append((x - half_w, x + half_w, y - half_h, y + half_h))

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
                    rx <= self.arena["xmin"]
                    or rx >= self.arena["xmax"]
                    or ry <= self.arena["ymin"]
                    or ry >= self.arena["ymax"]
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
        """Place a new simulated marker in the world at (x, y) or a random obstacle-free location."""
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
                (px - self.arena["xmin"]) < wall_margin
                or (self.arena["xmax"] - px) < wall_margin
                or (py - self.arena["ymin"]) < wall_margin
                or (self.arena["ymax"] - py) < wall_margin
            )

        # Robot position, used to avoid spawning too close
        rx, ry = self.state.odom.x, self.state.odom.y

        if x is not None and y is not None:
            if is_inside_obstacle(x, y):
                print(
                    f"[WARN] Tried to place marker inside obstacle at ({x:.2f}, {y:.2f}), ignored."
                )
                return
            if is_near_wall(x, y):
                print(
                    f"[WARN] Tried to place marker too close to wall at ({x:.2f}, {y:.2f}), ignored."
                )
                return
            self.markers = [(x, y)]
            return

        # --- Random placement with obstacle rejection ---
        max_attempts = 50
        buffer = 0.3
        for attempt in range(max_attempts):
            x = random.uniform(self.arena["xmin"] + buffer, self.arena["xmax"] - buffer)
            y = random.uniform(self.arena["ymin"] + buffer, self.arena["ymax"] - buffer)

            too_close_to_robot = math.hypot(x - rx, y - ry) < 0.5
            if is_inside_obstacle(x, y) or is_near_wall(x, y) or too_close_to_robot:
                continue

            # Valid spot
            self.markers = [(x, y)]
            print(f"Placed hex at ({x:.2f}, {y:.2f}) after {attempt + 1} attempts")
            return

        print("[WARN] Failed to find obstacle-free location for marker after many attempts.")

    def _update_markers(self):
        """Compute marker poses relative to the robot body frame."""
        from ..data.type_maps import Pose, PoseArray

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
        s.seen_hexes = PoseArray(poses=rel_poses)

    def read_all(self):
        return self.state

    def reset(self):
        self.state = SensorData()
        self.last_t = time.time()
