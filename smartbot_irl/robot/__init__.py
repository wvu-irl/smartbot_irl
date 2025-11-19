from typing import TypeAlias

# from . import smartbot_base, smartbot_real, smartbot_sim
from .smartbot import SmartBot

# from .smartbot_base import SmartBotBase
from .smartbot_real import SmartBotReal
from .smartbot_sim import SmartBotSim

SmartBotType: TypeAlias = SmartBotReal | SmartBotSim

__all__ = ['SmartBot', 'SmartBotReal', 'SmartBotSim', 'SmartBotType']
