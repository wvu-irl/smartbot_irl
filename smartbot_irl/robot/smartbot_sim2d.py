# smartbot_sim.py
from ..sim2d import SmartWorld, run_sim
from .smartbot_base import SmartBotBase, SmartBotBackend
import pygame
import time
import math
from ..data import JointState, SensorData, Command
from ..drawing import Drawer
from ..sim2d import SmartWorld
import multiprocessing as mp
from queue import Empty
from ..utils import SmartLogger
import logging

logger = SmartLogger(level=logging.INFO)  # Print statements, but better!


class SmartBotSim2d(SmartBotBackend):
    """Sim2d engine wrapper"""

    def __init__(
        self, drawing=True, smartbot_num=0, draw_region=((-5, 5), (-5, 5)), **kwargs
    ) -> None:
        self.sensor_data = SensorData()

        self.drawer = (
            Drawer(sensor_getter=lambda: self.sensor_data, region=draw_region) if drawing else None
        )

        ctx = mp.get_context('spawn')

        self.cmd_queue = ctx.Queue()
        self.out_queue = ctx.Queue()

        # Start simulator process
        self.sim_proc = ctx.Process(
            target=run_sim, args=(self.cmd_queue, self.out_queue), daemon=True
        )
        self.sim_proc.start()

    # def init(self, **kwargs) -> None:

    def write(self, cmd: Command) -> None:
        self.cmd_queue.put_nowait(cmd)

    def read(self) -> SensorData:
        # Get sensor data from sim.
        # logger.debug('Getting sensor data from sim2d', rate=5)
        # # Always read latest sensor packet first
        # msg = self.read()
        # if msg is not None:
        #     self.sensor_data = msg
        try:
            self.sensors = self.out_queue.get_nowait()
            # logger.debug(self.sensors, rate=4)
        except Empty:
            return None  # pyright: ignore[reportReturnType]
        return self.sensors

    def spin(self, dt: float = 0.05) -> None:
        # read latest data if available
        try:
            msg = self.out_queue.get_nowait()
            self.sensor_data = msg
        except Empty:
            pass

        # now draw
        if self.drawer and self.drawer._running:
            logger.info('drawing!', rate=1)
            self.drawer.draw_once(dt)

    def shutdown(self) -> None:
        """
        Clean up
        """
        self.sim_proc.terminate()
        self.sim_proc.join()

        self._running = False
        if self.drawer:
            self.drawer.quit()
