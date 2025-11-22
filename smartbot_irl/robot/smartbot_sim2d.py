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
        # self.sensor_data = SensorData()
        self.sensor_data = SensorData()
        self.drawer = Drawer(sensor_getter=self._get_data, region=draw_region) if drawing else None

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

    def _get_data(self) -> SensorData:
        return self.sensor_data

    def read(self) -> SensorData:
        """Return the current data."""

        if self.sensor_data is not None:
            return self.sensor_data
        return self.sensor_data

    def spin(self, dt: float = 0.05) -> None:
        # read latest data if available
        try:
            msg = self.out_queue.get_nowait()
            logger.debug(f'Got message {msg} of type {type(msg)}')
            self.sensor_data = msg
        except Empty:
            logger.debug('got enmpty message in spin')
            pass

        # now draw
        if self.drawer and self.drawer._running:
            logger.info(f'drawing! {self.sensor_data.odom.x}', rate=1)
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
