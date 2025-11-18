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


def _smartbot_factory(
    mode: str = 'real', drawing: bool = False, **kwargs
) -> Union[SmartBotReal, SmartBotSim]:
    """Internal factory returning SmartBotSim or SmartBotReal."""
    if mode == 'sim':
        return SmartBotSim(drawing=drawing, **kwargs)
    return SmartBotReal(drawing=drawing, **kwargs)


def SmartBot(  # noqa: D401  # pyright: ignore[reportRedeclaration]
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


class SmartBot:
    """
    High-level SmartBot interface.

    This is a convenience entry point that constructs either
    :class:`~smartbot_irl.robot.SmartBotReal` or
    :class:`~smartbot_irl.robot.SmartBotSim`
    depending on the mode.  It behaves like a class for users,
    even though it is implemented as a factory.

    Parameters
    ----------
    mode : {'real', 'sim'}
        Backend to instantiate.

    drawing : bool, optional
        Enable drawing/visualization.

    **kwargs
        Passed directly into the selected backend constructor.

    Returns
    -------
    Union[SmartBotReal, SmartBotSim]
        Concrete backend instance.
    """

    def __new__(cls, mode='real', drawing=False, **kwargs):
        return _smartbot_factory(mode=mode, drawing=drawing, **kwargs)

    # pass  # Sphinx sees this as the class.


# SmartBot.__doc__ = None  # Hide from autodoc
