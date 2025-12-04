from abc import ABC, abstractmethod
import logging
from typing import Type

from smartbot_irl.utils import SmartLogger
from ..data import SensorData
from typing import overload, Literal, Union

from .smartbot_sim import SmartBotSim
from .smartbot_sim2d import SmartBotSim2d
from .smartbot_real import SmartBotReal
from .smartbot_base import SmartBotBase

from ..data import Command

logger = SmartLogger(level=logging.DEBUG)  # Print statements, but better!


class SmartBot:
    def __init__(
        self,
        ip: str | None = None,
        mode='sim2d',
        drawing=False,
        smartbot_num=0,
        draw_region=((-5, 5), (-5, 5)),
        **kwargs,
    ):
        if mode == 'real':
            if ip is None or smartbot_num == 0:
                logger.error('Please specify robot IP and smartbot number')
                return
            self.backend = SmartBotReal(
                draw_region=draw_region, smartbot_num=smartbot_num, drawing=drawing, ip=ip
            )
        elif mode == 'sim2d':
            self.backend = SmartBotSim2d()

    def init(self, **kwargs) -> None: ...
    def read(self) -> SensorData:
        return self.backend.read()

    def write(self, command: Command) -> None:
        """Send commands to the smartbot.

        Parameters
        ----------
            command : Command
                An instance of `smartbot_irl.Command`. Default values of data
                attributes will be zeros, empty strings, etc.
        """
        self.backend.write(command)

    def spin(self) -> None:
        self.backend.spin()

    def shutdown(self) -> None:
        self.backend.shutdown()

    def place_hex(self, *a, **kw):
        # Does nothing for real robot
        raise NotImplementedError
