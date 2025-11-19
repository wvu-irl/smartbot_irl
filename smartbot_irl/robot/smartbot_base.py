from abc import ABC, abstractmethod
from typing import Tuple
from ..data import Command, SensorData
from ..sim2d.engine import SimEngine


class SmartBotBase(ABC):
    """Abstract base defining the robot interface."""

    engine: SimEngine | None
    """Underlying simulation engine (sim backends only)."""

    def __init__(self, draw_region: Tuple = ((0, 0), (3, 3)), drawing=False):
        self.drawing = drawing

    @abstractmethod
    def init(self, **kwargs) -> None: ...
    @abstractmethod
    def read(self) -> SensorData: ...
    @abstractmethod
    def write(self, command: Command) -> None:
        """Send commands to the smartbot.

        Parameters
        ----------
            command : Command
                An instance of `smartbot_irl.Command`. Default values of data
                attributes will be zeros, empty strings, etc.
        """
        ...

    @abstractmethod
    def spin(self) -> None: ...
    @abstractmethod
    def shutdown(self) -> None: ...
    # Non-mandatory extensions.
    def place_hex(self, *a, **kw):
        raise NotImplementedError
