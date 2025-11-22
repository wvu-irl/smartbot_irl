import math
import pygame
from typing import Callable
from ..data import SensorData


class Drawer:
    """
    Non-threaded drawer that visualizes a SmartBot's pose.
    Called explicitly each frame from the main simulation loop.
    """

    def __init__(
        self,
        sensor_getter: Callable[[], SensorData],
        scale: float = 80.0,
        window_size=(800, 800),
        region=((-3, 3), (-3, 3)),
    ):
        """

        Args:
            region (tuple(tuple)): Rectangular region defined by two points to be visualized.
        """
        self._get = sensor_getter
        self.scale = scale
        self.show_hud = True

        (xmin, xmax), (ymin, ymax) = region
        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax

        world_w = xmax - xmin
        world_h = ymax - ymin

        # ---- window (pixels) ----
        win_w, win_h = window_size
        self.win_w, self.win_h = win_w, win_h

        # ---- auto-scale: fit region exactly inside window ----
        # one world meter maps to: pixels_per_meter
        sx = win_w / world_w
        sy = win_h / world_h
        self.scale = min(sx, sy)  # preserve aspect ratio

        # Compute window size in pixels from region & scale
        width_px = int(world_w * scale)
        height_px = int(world_h * scale)

        pygame.init()
        self.screen = pygame.display.set_mode((win_w, win_h))
        pygame.display.set_caption('SmartBot Viewer')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('monospace', 16)
        self._running = True

    def world_to_screen(self, x, y):
        # subtract region mins AND flip y axis
        sx = int((x - self.xmin) * self.scale)
        sy = int((self.ymax - y) * self.scale)
        return sx, sy

    def draw_once(self, dt: float = 0.01):
        """Draws everything the robot can see."""
        d = self._get()

        scan = d.scan
        # Check if we have received an odometry message yet.
        if d is None or d.odom is None or d.scan is None:
            print('waiting for odom and scan...')
            return
        x, y, theta = d.odom.x, d.odom.y, d.odom.yaw

        # Clear
        self.screen.fill((25, 25, 25))

        # Convert to screen coordinates
        cx, cy = self.world_to_screen(x, y)

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
            for pose, id in zip(markers.poses, markers.marker_ids):
                # Marker is in robot frame → transform to world
                rel_x, rel_y = pose.x, pose.y
                mx_world = d.odom.x + math.cos(theta) * rel_x - math.sin(theta) * rel_y
                my_world = d.odom.y + math.sin(theta) * rel_x + math.cos(theta) * rel_y

                mx = 400 + int(self.scale * mx_world)
                my = 400 - int(self.scale * my_world)

                pygame.draw.rect(
                    self.screen, (255, 180, 0), pygame.Rect(mx - 6, my - 6, 12, 12), 7
                )
                label = self.font.render(f'{id}', True, (255, 163, 33))
                self.screen.blit(label, (mx + 8, my))

        # Draw robot body
        pygame.draw.circle(self.screen, (255, 230, 0), (cx, cy), 0.1 * self.scale)

        # Draw heading line
        hx = cx + int(0.5 * self.scale * math.cos(theta))
        hy = cy - int(0.5 * self.scale * math.sin(theta))
        pygame.draw.line(self.screen, (255, 50, 50), (cx, cy), (hx, hy), 3)

        if self.show_hud:
            instructions = (
                'Controls:\n'
                '  ↑ ↓ : Forward / Back\n'
                '  ← → : Rotate\n'
                '  B/N/M : Arm presets\n'
                '  h   : Toggle menus\n'
                '  q   : Quit'
            )

            draw_text_block(
                self.screen,
                instructions,
                pos=(10, 10),
                font=self.font,
                color=(230, 230, 230),
                bg_color=(40, 40, 40),  # soft dark background
                line_spacing=2,
                padding=8,
            )
            state_str = f'Pose:\n  x={x:+.2f}\n  y={y:+.2f}\n  theta={theta:+.2f}\n  Gripper{d.gripper_curr_state}\n  Manipulator{d.manipulator_curr_preset}'

            draw_text_block(
                self.screen,
                state_str,
                pos=(400, 10),
                font=self.font,
                color=(200, 200, 200),
                bg_color=(20, 20, 20),
            )

        pygame.display.flip()
        self.clock.tick(int(1 / dt))

    def quit(self):
        pygame.quit()


def draw_text_block(
    surface,
    text_lines,
    pos=(10, 10),
    font=None,
    color=(220, 220, 220),
    line_spacing=4,
    bg_color=None,
    padding=6,
):
    """
    Draw a block of multi-line text with optional background.

    text_lines: list[str] or a single string with '\n'
    """
    if isinstance(text_lines, str):
        text_lines = text_lines.split('\n')

    if font is None:
        raise ValueError('Font must be supplied')

    x, y = pos

    # Compute total height for block background
    rendered = [font.render(line, True, color) for line in text_lines]
    widths = [surf.get_width() for surf in rendered]
    heights = [surf.get_height() for surf in rendered]

    block_w = max(widths) + 2 * padding
    block_h = sum(heights) + line_spacing * (len(heights) - 1) + 2 * padding

    # Draw background rectangle if requested
    if bg_color is not None:
        pygame.draw.rect(surface, bg_color, (x, y, block_w, block_h), border_radius=6)

    # Draw text lines
    tx = x + padding
    ty = y + padding

    for surf in rendered:
        surface.blit(surf, (tx, ty))
        ty += surf.get_height() + line_spacing
