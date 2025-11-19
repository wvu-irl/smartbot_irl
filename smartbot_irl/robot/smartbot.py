from typing import Type
from ..data import SensorData
from typing import overload, Literal, Union

from .smartbot_sim import SmartBotSim
from .smartbot_real import SmartBotReal
from .smartbot_base import SmartBotBase


@overload
def SmartBot(mode: Literal['real'], drawing: bool = False, **kwargs) -> SmartBotReal: ...


@overload
def SmartBot(mode: Literal['sim'], drawing: bool = False, **kwargs) -> SmartBotSim: ...


def SmartBot(
    mode: str = 'real', drawing: bool = False, **kwargs
) -> Union[SmartBotReal, SmartBotSim]:
    """
    Create either a real or simulated SmartBot.

    Parameters
    ----------
        mode : {'real', 'sim'}, optional
            Which backend to construct.

            * ``'real'`` → :class:`~smartbot_irl.robot.SmartBotReal`
            * ``'sim'`` → :class:`~smartbot_irl.robot.SmartBotSim`

        drawing : bool, optional
            Enable drawing or visualization.

        **kwargs
            Passed directly to the selected backend constructor.

    Returns
    -------
        SmartBotReal or SmartBotSim

    Examples
    --------
        >>> bot = SmartBot('sim')
        >>> bot = SmartBot('real')
    """
    if mode == 'sim':
        return SmartBotSim(drawing=drawing, **kwargs)
    else:
        return SmartBotReal(drawing=drawing, **kwargs)
