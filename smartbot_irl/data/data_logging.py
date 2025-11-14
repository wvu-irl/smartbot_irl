#data_logging.py
from dataclasses import dataclass, field
from datetime import datetime
from time import time
from types import SimpleNamespace
import pandas as pd
"""
This class should take a list of strings to make new columns for. Then it should
offer intellisense for these columns. This will make it so students can
configure the state object to have a dataframe in the way they want it. But they
don't need to look at any pandas stuff. But it is a subclass so theyn can still
use .to_csv and .plot().

Pandas unfortunately does not have a good way to add extra attributes outside of
the dataframe so we just shove them in with a class that wraps the dataframe
proper.
"""
@dataclass
class State:
    state_vec: pd.DataFrame = field(init=False)
    next_index: int = field(default=0, init=False)

    def __post_init__(self):
        # Create an empty DataFrame
        self.state_vec = pd.DataFrame()
        # self.state_vec = pd.DataFrame(columns=[
        #     "t_epoch", "time", "t_prev", "t_elapsed", "turning",
        #     "x", "y"  # if you want these to exist for plotting
        # ])

        #TODO init first row in student code.
        seed = {
            "t_epoch": time(),
            "t": 0.0,
            "time": 0.0,
            "t_prev": time(),
            "t_elapsed": 0.0,
            "turning": False,
        }
        self.append_row(seed)

    def append_row(self, rowdict: dict):
        # Build the row DataFrame
        row_df = pd.DataFrame([rowdict])

        # Concat first
        self.state_vec = pd.concat([self.state_vec, row_df], ignore_index=True)

        # Only after concat do we back-fill any missing columns
        # (Pandas will align for new columns automatically)
        for col in rowdict:
            if col not in self.state_vec.columns:
                self.state_vec[col] = pd.NA


    @property
    def last(self) -> SimpleNamespace:
        return SimpleNamespace(**self.state_vec.iloc[-1].to_dict())

    def __getattr__(self, name):
        # Prevent recursion: if 'state_vec' is missing, raise
        if name == "state_vec":
            raise AttributeError
        return getattr(self.state_vec, name)

    def __getitem__(self, key):
        return self.state_vec[key]

    def __setitem__(self, key, value):
        self.state_vec[key] = value


def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")