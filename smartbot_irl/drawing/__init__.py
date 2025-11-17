"""package level pydoc for smartbot_irl.drawing"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from ._drawer_thread import Drawer
from ._plotting import PlotManager, FigureWrapper

__all__ = []
