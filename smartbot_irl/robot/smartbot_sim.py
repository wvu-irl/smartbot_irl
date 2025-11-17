# smartbot_sim.py
from .smartbot_base import SmartBotBase
import pygame
import time
import math
from ..data import JointState, SensorData, Command
from ..drawing import Drawer
from ..sim2d.engine import SimEngine
from ..sim2d.sensors import SimSensors
from ..utils import SmartLogger
import logging

logger = SmartLogger(level=logging.INFO)  # Print statements, but better!


class SmartBotSim(SmartBotBase):
    def __init__(self, drawing=False, smartbot_num=0, draw_region=((-5, 5), (-5, 5))):
        super().__init__(drawing=drawing, draw_region=draw_region)
        self.engine = SimEngine()

        self.engine.add_obstacle(1.0, 0.0, 1.0, 0.5)
        self.engine.add_obstacle(-2.0, 2.0, 0.5, 0.5)
        self.engine.add_obstacle(-3.0, -2.0, 0.1, 2.5)

        self.sensor_data = self.engine.read_all()  # start with engine’s data
        self.drawer = Drawer(lambda: self.sensor_data, region=draw_region) if drawing else None
        self._running = False

    def init(self, **kwargs):
        logger.info(msg='Connecting to smartbot...')
        logger.info(msg='Connecting connected !')

        self._running = True
        s = self.engine.state

        # Setup 2-wheel diff drive joint data
        s.joints = JointState()
        s.joints.names = ['left_wheel', 'right_wheel']
        s.joints.positions = [0.0, 0.0]
        s.joints.velocities = [0.0, 0.0]

        # Initialize odometry.
        s.odom.x = 0.0
        s.odom.y = 0.0
        s.odom.yaw = 0.0

        scan = s.scan
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.radians(5.0)
        num_rays = int((scan.angle_max - scan.angle_min) / scan.angle_increment)
        scan.ranges = [float('inf')] * num_rays

        print('SmartBotSim initialized')

    def place_hex(self, x=None, y=None):
        self.engine.place_hex(x, y)

    def write(self, cmd: Command):
        self.engine.apply_command(cmd)

    def read(self) -> SensorData:
        # Get sensor data from sim.
        self.sensor_data = self.engine.read_all()
        return self.sensor_data

    def spin(self, dt: float = 0.05):
        self.engine.step(dt)
        self.read()  # Update sensor data.
        if self.drawer and self.drawer._running:
            self.drawer.draw_once(dt)
        # time.sleep(dt)

    def shutdown(self):
        r"""
        Clean up roslibpy and pygame objects.
        """
        self._running = False
        if self.drawer:
            self.drawer.quit()
