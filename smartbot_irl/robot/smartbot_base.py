from abc import ABC, abstractmethod
from ..data import Command, SensorData

class SmartBotBase(ABC):
    """Abstract base defining the robot interface."""

    def __init__(self, drawing=False):
        self.drawing = drawing

    @abstractmethod
    def init(self, **kwargs): ...
    @abstractmethod
    def read(self) -> SensorData: ...
    @abstractmethod
    def write(self, command: Command): ...
    @abstractmethod
    def spin(self): ...
    @abstractmethod
    def shutdown(self): ...
    # Non-mandatory extensions.
    def place_hex(self, *a, **kw): raise NotImplementedError

