from abc import ABC, abstractmethod
from typing import Type
from ..data import SensorData
from typing import overload, Literal, Union

from .smartbot_sim import SmartBotSim
from .smartbot_sim2d import SmartBotSim2d
from .smartbot_real import SmartBotReal
from .smartbot_base import SmartBotBase

from ..data import Command


# class SmartBot:
#     def __init__(
#         self,
#         mode='sim2d',
#         drawing=False,
#         smartbot_num=0,
#         draw_region=((-5, 5), (-5, 5)),
#         **kwargs,
#     ):
#         if mode == 'real':
#             self.engine = SmartBotReal()
#         elif mode == 'sim2d':
#             self.engine = SmartBotSim2d()

#     def init(self, **kwargs) -> None: ...
#     def read(self) -> SensorData:
#         return self.engine.read()

#     def write(self, command: Command) -> None:
#         """Send commands to the smartbot.

#         Parameters
#         ----------
#             command : Command
#                 An instance of `smartbot_irl.Command`. Default values of data
#                 attributes will be zeros, empty strings, etc.
#         """
#         self.backend.write(command)

#     def spin(self) -> None:
#         self.backend.spin()

#     def shutdown(self) -> None:
#         self.backend.shutdown()

#     def place_hex(self, *a, **kw):
#         # Does nothing for real robot
#         raise NotImplementedError


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
            Which engine to construct.

            * ``'real'`` → :class:`~smartbot_irl.robot.SmartBotReal`
            * ``'sim'`` → :class:`~smartbot_irl.robot.SmartBotSim`

        drawing : bool, optional
            Enable drawing or visualization.

        **kwargs
            Passed directly to the selected engine constructor.

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


def SmartBot(
    mode: str = 'sim2d', drawing: bool = False, **kwargs
) -> Union[SmartBotReal, SmartBotSim]:
    """
    Create either a real or simulated SmartBot.

    Parameters
    ----------
        mode : {'real', 'sim2d', 'mujo'}, optional
            Which engine to use..

            * ``'real'`` Real ros2 robot
            * ``'sim2d'`` 2D simulator
            * ``'mujo'`` Mujoco based simulator

        drawing : bool, optional
            Enable drawing or visualization.

        **kwargs
            Passed directly to the selected engine constructor.

    Returns
    -------
        SmartBotReal or SmartBotSim

    Examples
    --------
        >>> bot = SmartBot('sim2d')
        >>> bot = SmartBot('real')
    """
    if mode == 'sim':
        return SmartBotSim(drawing=drawing, **kwargs)
    else:
        return SmartBotReal(drawing=drawing, **kwargs)
