# smartbot_irl/robot.smartbot.py
from typing import Literal, Union, overload

from .smartbot_real import SmartBotReal
from .smartbot_sim import SmartBotSim


@overload
def SmartBot(mode: Literal['real'], drawing: bool = False, **kwargs) -> SmartBotReal: ...
@overload
def SmartBot(mode: Literal['sim'], drawing: bool = False, **kwargs) -> SmartBotSim: ...
def SmartBot(
    mode: str = 'real', drawing: bool = False, **kwargs
) -> Union[SmartBotReal, SmartBotSim]:
    """Factory that returns a SmartBotReal or SmartBotSim instance."""
    if mode == 'sim':
        return SmartBotSim(drawing=drawing, **kwargs)
    else:
        return SmartBotReal(drawing=drawing, **kwargs)
