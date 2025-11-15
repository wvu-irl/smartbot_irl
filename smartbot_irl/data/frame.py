import pandas as pd
import numpy as np


class Frame(pd.DataFrame):
    """A DataFrame that auto-grows and allows both Series and per-row dot access."""

    _metadata = ["_next_row", "_capacity", "_grow_factor"]

    def __init__(self, *args, columns=None, init_capacity=1000, grow_factor=2.0, **kwargs):
        if not args and columns is None:
            columns = self._default_columns()
        super().__init__(np.full((init_capacity, len(columns)), pd.NA), columns=columns, **kwargs)
        self._capacity = init_capacity
        self._next_row = 0
        self._grow_factor = grow_factor

    # --------------------------------------------------------------
    def _default_columns(self):
        """Hook for subclasses: infer from __annotations__."""
        if hasattr(self, "__annotations__"):
            return list(self.__annotations__.keys())
        return []

    # --------------------------------------------------------------
    def __getitem__(self, key):
        if not isinstance(key, int):
            return super().__getitem__(key)
        if key < 0:
            key = self._next_row + key
        if key >= self._next_row:
            self._ensure_capacity(key + 1)
            self._next_row = key + 1
        return _RowProxy(self, key)

    def _ensure_capacity(self, needed):
        if needed <= self._capacity:
            return
        new_capacity = int(max(needed, self._capacity * self._grow_factor))
        extra = pd.DataFrame(
            np.full((new_capacity - self._capacity, len(self.columns)), pd.NA),
            columns=self.columns,
        )
        self._capacity = new_capacity
        super(Frame, self).__init__(pd.concat([self, extra], ignore_index=True))

    @property
    def used(self):
        """Return the portion of the DataFrame actually filled."""
        return self.iloc[: self._next_row]

    # --------------------------------------------------------------
    def __getattr__(self, name):
        """Make df.col work like df['col'] if it exists."""
        # Avoid recursion and metadata
        if name in self.columns:
            return self[name]
        raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")


class _RowProxy:
    """Per-row dot-access wrapper."""

    def __init__(self, parent: Frame, idx: int):
        object.__setattr__(self, "parent", parent)
        object.__setattr__(self, "idx", idx)

    def __getattr__(self, col):
        if col not in self.parent.columns:
            raise AttributeError(f"No column '{col}'")
        return self.parent.at[self.idx, col]

    def __setattr__(self, col, val):
        if col in ("parent", "idx"):
            object.__setattr__(self, col, val)
            return
        if col not in self.parent.columns:
            self.parent[col] = pd.NA
        self.parent.at[self.idx, col] = val

    def __repr__(self):
        return repr(self.parent.loc[self.idx])
