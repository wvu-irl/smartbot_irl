from . import smartbot_base, smartbot_real, smartbot_sim
from .smartbot_base import SmartBotBase
from .smartbot_real import SmartBotReal
from .smartbot_sim import SmartBotSim
from .smartbot import SmartBot

from typing import TypeAlias

SmartBotType: TypeAlias = SmartBotReal | SmartBotSim

__all__ = [
    "SmartBot",
]
