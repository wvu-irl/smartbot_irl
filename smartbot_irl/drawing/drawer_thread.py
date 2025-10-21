import threading
import time
import math
import pygame
from typing import Callable, Optional
from ..data import SensorData


class Drawer:
    """
    Non-threaded drawer that visualizes a SmartBot's pose.
    Called explicitly each frame from the main simulation loop.
    """

    def __init__(self, sensor_getter: Callable[[], SensorData], scale: float = 80.0):
        self._get = sensor_getter
        self.scale = scale

        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("SmartBot Viewer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self._running = True

    def draw_once(self, dt: float = 0.01):
        """Call this every frame from your main loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

        d = self._get()

        scan = d.scan
        # Check if we have received an odometry message yet.
        if d is None or d.odom is None or d.scan is None:
            print("waiting for odom and scan...")
            return
        x, y, theta = d.odom.x, d.odom.y, d.odom.yaw

        # Clear
        self.screen.fill((25, 25, 25))

        # Convert to screen coordinates
        cx = 400 + int(x * self.scale)
        cy = 400 - int(y * self.scale)

        # Data Source is raw lidar.
        if scan.ranges:
            # Precompute angles
            n = len(scan.ranges)
            angles = [scan.angle_min + i * scan.angle_increment for i in range(n)]

            # Transform scan points into global coordinates (relative to robot pose)
            points = []
            for r, a in zip(scan.ranges, angles):
                if r is None:
                    continue
                if r <= 0.01 or math.isinf(r) or math.isnan(r):
                    continue
                # laser angle is relative to robot heading
                gx = cx + int(self.scale * r * math.cos(theta + a))
                gy = cy - int(self.scale * r * math.sin(theta + a))
                points.append((gx, gy))

            # Draw all points
            if points:
                # draw a small dot at the robot origin
                pygame.draw.circle(self.screen, (0, 255, 0), (cx, cy), 3)

                # draw each scan ray as a short green line from robot center to hit point
                for gx, gy in points:
                    pygame.draw.line(self.screen, (0, 255, 0), (cx, cy), (gx, gy), 1)

        # Draw ArUco markers if any
        # markers = getattr(d, "aruco_poses", None)
        # print(d.aruco_poses)
        if d.seen_hexes and d.seen_hexes.poses:
            markers = d.seen_hexes
            # print(markers)
            for pose in markers.poses:
                # Marker is in robot frame → transform to world
                rel_x, rel_y = pose.x, pose.y
                mx_world = d.odom.x + math.cos(theta) * rel_x - math.sin(theta) * rel_y
                my_world = d.odom.y + math.sin(theta) * rel_x + math.cos(theta) * rel_y

                mx = 400 + int(self.scale * mx_world)
                my = 400 - int(self.scale * my_world)

                pygame.draw.rect(self.screen, (255, 180, 0), pygame.Rect(mx - 6, my - 6, 12, 12), 2)
                label = self.font.render("aruco", True, (255, 200, 50))
                self.screen.blit(label, (mx + 8, my))

        # Draw robot body
        pygame.draw.circle(self.screen, (255, 230, 0), (cx, cy), 30)

        # Draw heading line
        hx = cx + int(20 * math.cos(theta))
        hy = cy - int(20 * math.sin(theta))
        pygame.draw.line(self.screen, (255, 50, 50), (cx, cy), (hx, hy), 3)

        # Draw text overlay
        pose_str = f"x={x:+.2f}  y={y:+.2f}  θ={theta:+.2f}"
        text_surf = self.font.render(pose_str, True, (180, 180, 180))
        self.screen.blit(text_surf, (10, 10))

        pygame.display.flip()
        self.clock.tick(int(1 / dt))

    def quit(self):
        pygame.quit()
