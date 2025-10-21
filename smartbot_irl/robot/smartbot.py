from typing import Type
from smartbot_irl.data.data import SensorData
from typing import overload, Literal, Union

from .smartbot_sim import SmartBotSim
from .smartbot_real import SmartBotReal
from .smartbot_base import SmartBotBase


# class SmartBot(SmartBotBase):
#     """Returns correct class and makes static analysis work."""

#     def __new__(cls, mode: str = "real", **kwargs) -> SmartBotBase:
#         if mode == "sim":
#             subclass: Type[SmartBotBase] = SmartBotSim
#         else:
#             subclass = SmartBotReal
#         instance = object.__new__(subclass)
#         subclass.__init__(instance, **kwargs)
#         return instance

@overload
def SmartBot(mode: Literal["real"], drawing: bool = False, **kwargs) -> SmartBotReal: ...
@overload
def SmartBot(mode: Literal["sim"], drawing: bool = False, **kwargs) -> SmartBotSim: ...
def SmartBot(mode: str = "real", drawing: bool = False, **kwargs) -> Union[SmartBotReal, SmartBotSim]:
    """Factory that returns a SmartBotReal or SmartBotSim instance."""
    if mode == "sim":
        return SmartBotSim(drawing=drawing, **kwargs)
    else:
        return SmartBotReal(drawing=drawing, **kwargs)

# class SmartBot:
#     """Factory that returns a SmartBotReal or SmartBotSim instance."""

#     def __new__(cls, mode='real', drawing=False, **kwargs):
#         if mode == 'sim':
#             return SmartBotSim(drawing=drawing, **kwargs)
#         else:
#             return SmartBotReal(drawing=drawing, **kwargs)
