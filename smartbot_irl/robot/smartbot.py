from typing import Type
from ..data import SensorData
from typing import overload, Literal, Union

from .smartbot_sim import SmartBotSim
from .smartbot_real import SmartBotReal
from .smartbot_base import SmartBotBase


@overload
def SmartBot(mode: Literal["real"], drawing: bool = False, **kwargs) -> SmartBotReal: ...
@overload
def SmartBot(mode: Literal["sim"], drawing: bool = False, **kwargs) -> SmartBotSim: ...
def SmartBot(
    mode: str = "real", drawing: bool = False, **kwargs
) -> Union[SmartBotReal, SmartBotSim]:
    """Factory that returns a SmartBotReal or SmartBotSim instance."""
    if mode == "sim":
        return SmartBotSim(drawing=drawing, **kwargs)
    else:
        return SmartBotReal(drawing=drawing, **kwargs)
