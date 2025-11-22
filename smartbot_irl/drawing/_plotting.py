import queue
from socket import timeout
from time import time, sleep

import matplotlib
from multiprocessing import Process, Queue

from smartbot_irl.utils import SmartLogger, logging

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

logger = SmartLogger(level=logging.CRITICAL)  # Print statements, but better!

# matplotlib.use("TkAgg")
import pandas as pd
from matplotlib.gridspec import GridSpec

STOP_SIGNAL = 'STOP'


class FigureWrapper:
    def __init__(self, max_fps=30, **kwargs):
        self.fig = plt.figure()
        self.axes = []

        self._title = kwargs.pop('title', None)  # store it
        if self._title:
            self.fig.suptitle(self._title)

        self._fig_kwargs = kwargs
        self._apply_fig_kwargs()
        self.items = []  # (kind, artist, x_col, y_col)
        self.last_draw = 0
        self.min_dt = 1.0 / max_fps

    def _apply_fig_kwargs(self):
        """Applies kwargs to figure if figure has matching set_* methods."""
        for k, v in self._fig_kwargs.items():
            setter = f'set_{k}'
            if hasattr(self.fig, setter):
                getattr(self.fig, setter)(v)
            else:
                raise ValueError(f"{self.fig} does not accept figure kwarg '{k}'")

    from matplotlib.gridspec import GridSpec

    def _new_subplot(self):
        # TODO handle remaking subplots without breaking legends.
        n = len(self.axes) + 1

        # Build a new gridspec with n rows
        gs = GridSpec(n, 1, figure=self.fig)

        # Reassign existing axes to their correct grid position
        for i, ax in enumerate(self.axes):
            ax.set_subplotspec(gs[i, 0])
            ax.set_position(gs[i, 0].get_position(self.fig))

        # Create and place the new axis
        ax_new = self.fig.add_subplot(gs[n - 1, 0])
        self.axes.append(ax_new)

        return ax_new

    def _apply_kwargs(self, target, kwargs):
        """Applies kwargs to target if target has a matching set_* method."""
        for k, v in kwargs.items():
            setter = f'set_{k}'
            if hasattr(target, setter):
                getattr(target, setter)(v)
            else:
                raise ValueError(f"{target} does not accept kwarg '{k}'")

    def _expand_yval(self, yval):
        """
        Normalize a y-value into a list of scalars.
        Accepts scalars, lists, numpy arrays, pandas Series.
        """
        if np.isscalar(yval):
            return [float(yval)]  # pyright: ignore[reportArgumentType]

        if isinstance(yval, (list, tuple, np.ndarray, pd.Series)):
            # Convert numpy/pandas objects to python floats
            return [float(v) for v in yval]

        raise TypeError(f'Unsupported y-value type: {type(yval)}')

    def add_line(self, x_col=None, y_col=None, window=30, **kwargs):
        if y_col is None:
            raise ValueError('y_col must be specified')

        # Always create a new subplot
        ax = self._new_subplot()

        # Normalize y_col to a list
        # y_col is a list of column names
        # but the actual row values may themselves be lists!
        y_col_list = [y_col] if not isinstance(y_col, list) else list(y_col)

        # Split kwargs into artist kwargs vs axes kwargs
        artist_kwargs = {}
        axes_kwargs = {}

        for k, v in kwargs.items():
            setter = f'set_{k}'
            if hasattr(ax, setter):
                axes_kwargs[k] = v
            else:
                artist_kwargs[k] = v

        # Extract label(s)
        raw_labels = artist_kwargs.pop('labels', None)

        if raw_labels is None:
            # No labels provided → auto-generate None for all
            labels = [None] * len(y_col_list)
        elif isinstance(raw_labels, list):
            if len(raw_labels) != len(y_col_list):
                raise ValueError('label list length must match y_col list')
            labels = raw_labels
        else:
            # broadcast single label
            labels = [raw_labels] * len(y_col_list)

        raw_color = artist_kwargs.pop('color', None)
        if isinstance(raw_color, list):
            if len(raw_color) != len(y_col_list):
                raise ValueError('color list length must match y_col list')
            colors = raw_color
        else:
            colors = [raw_color] * len(y_col_list)

        artists = []
        for lbl, col in zip(labels, colors):
            ak = dict(artist_kwargs)
            if col is not None:
                ak['color'] = col
            if lbl is not None:
                ak['label'] = lbl

            (line,) = ax.plot([], [], **ak)
            artists.append([line])

        # Apply axes kwargs
        if axes_kwargs:
            self._apply_kwargs(ax, axes_kwargs)

        if any(lbl is not None for lbl in labels):
            ax.legend(handlelength=3)

        # For each y-col create its own buffer
        # buffers = [([], []) for _ in y_col_list]
        buffers = []
        for _ in y_col_list:
            buffers.append(([[]], [[]]))  # xbufs, ybufs: start with 1 empty trace

        # self.fig.tight_layout()
        self.fig.set_size_inches(10, 8, forward=True)
        self.fig.subplots_adjust(hspace=0.3)

        self.items.append((ax, 'line', artists, x_col, y_col_list, window, buffers))
        return artists

    def add_scatter(self, x_col=None, y_col=None, window=1000, **kwargs):
        # For scatter, still create marker-style line2D objects
        kwargs.setdefault('ls', '')
        kwargs.setdefault('marker', 'o')
        return self.add_line(x_col, y_col, window, **kwargs)

    def update(self, df_last_row: pd.Series) -> None:
        for ax, kind, artists, x_col, y_col_list, window, buffers in self.items:
            # Compute x once
            xval = df_last_row.name if x_col is None else df_last_row[x_col]

            # Iterate over y-cols
            for i, ycol in enumerate(y_col_list):
                xbufs, ybufs = buffers[i]
                line_list = artists[i]

                raw = df_last_row[ycol]

                # Normalize input into a list of floats
                if np.isscalar(raw):
                    yvals = [float(raw)]  # pyright: ignore[reportArgumentType]
                elif isinstance(raw, (list, tuple, np.ndarray, pd.Series)):
                    yvals = [float(v) for v in raw]
                else:
                    raise TypeError(f'Column {ycol} has unsupported type {type(raw)}')

                # Auto-expand if yvals is longer than existing lines
                if len(yvals) > len(line_list):
                    extra = len(yvals) - len(line_list)
                    for k in range(extra):
                        (new_line,) = ax.plot([], [], label=f'{ycol}[{len(line_list) + k}]')
                        line_list.append(new_line)
                        xbufs.append([])
                        ybufs.append([])
                    ax.legend()

                # Update each component
                for j, yval in enumerate(yvals):
                    xb = xbufs[j]
                    yb = ybufs[j]

                    xb.append(xval)
                    yb.append(yval)

                    if len(xb) > window:
                        xb.pop(0)
                    if len(yb) > window:
                        yb.pop(0)

                    line_list[j].set_data(xb, yb)
            # Calc X and Y limits
            xmin = float('inf')
            xmax = float('-inf')
            ymin = float('inf')
            ymax = float('-inf')

            for xbufs_i, ybufs_i in buffers:
                for xb in xbufs_i:
                    if xb:
                        vmin = min(xb)
                        vmax = max(xb)

                        if vmin < xmin:
                            xmin = vmin
                        if vmax > xmax:
                            xmax = vmax

                for yb in ybufs_i:
                    if yb:
                        vmin = min(yb)
                        vmax = max(yb)
                        if vmin < ymin:
                            ymin = vmin
                        if vmax > ymax:
                            ymax = vmax

            if xmin < xmax and xmin != float('inf'):
                span = xmax - xmin
                xpad = 0.05 * span if span > 0 else 1.0
                ax.set_xlim(xmin - xpad, xmax + xpad)

            if ymin < ymax and ymin != float('inf'):
                span = ymax - ymin
                ypad = 0.05 * span if span > 0 else 1
                ax.set_ylim(ymin - ypad, ymax + ypad)

    def update_all(self, new_row):
        for fw in self.figures:
            fw.update(new_row)
            fw.redraw_if_needed()

    def redraw_if_needed(self):
        now = time()
        if now - self.last_draw >= self.min_dt:
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            self.last_draw = now


class PlotManager:
    """Spawns process to handle matplotlib plotting."""

    def __init__(self, leave_plots=False):
        self.figures: list[FigureWrapper] = []
        # self.data_queue = Queue(maxsize=1)
        from multiprocessing import Manager

        self.manager = Manager()
        self.buffer = self.manager.list()  # shared list
        self.buffer_max = 16  # ring size

        self.leave_plots = leave_plots

    def add_figure(self, max_fps=30, **kwargs):
        fw = FigureWrapper(max_fps=max_fps, **kwargs)
        self.figures.append(fw)
        return fw

    def update_all(self, data: pd.Series) -> None:
        for fw in self.figures:
            fw.update(df_last_row=data)
            fw.redraw_if_needed()

    def update_queue(self, data: pd.Series):
        buf = self.buffer
        # evict oldest if at capacity
        if len(buf) >= self.buffer_max:
            buf.pop(0)
        buf.append(data)

    def draw_plots(self, data_queue: Queue, figs: list[FigureWrapper]):
        """To be called as a new process."""
        import signal as _signal

        # Ignore SIGINT in the plot process so Tk never sees KeyboardInterrupt.
        _signal.signal(_signal.SIGINT, _signal.SIG_IGN)

        plt.show(block=False)  # Make our plots appear.
        while True:
            # Pull oldest item if available
            if len(self.buffer) == 0:
                plt.pause(0.01)
                continue

            data: pd.Series | str = self.buffer.pop(0)

            # Catch stop signal from queue.
            if type(data) is str and data == STOP_SIGNAL:
                logger.warn('got STOP signal')
                break
            # else:
            # data: pd.Series

            # Redraw plots
            for fw in figs:
                # TODO fix type warning...
                fw.update(df_last_row=data)  # pyright: ignore[reportArgumentType]
                fw.redraw_if_needed()
            # logger.warn('Looping draw')
            sleep(0.001)

        if self.leave_plots:
            logger.info('Leaving plots open')
            plt.ioff()
            plt.show()
        else:
            logger.info('Closing plots')
            plt.close()

    def start_plot_proc(self):
        """_summary_"""
        self.plot_proc = Process(target=self.draw_plots, args=(None, self.figures))

        self.plot_proc.start()

    def stop_plot_proc(self):
        # Empty queue.
        try:
            self.buffer[:] = []
        except Exception:
            pass

        # Send 'STOP' on queue.
        # TODO Less hacky solution? Mixing types in queue here.
        try:
            logger.info('Sending stop to plot process...')
            self.data_queue.put_nowait(STOP_SIGNAL)
        except Exception:
            pass
        logger.warn('Joining child proc...')

        # Wait for plotting proc to die.
        self.plot_proc.join(timeout=0.3)

        # IF it doesn't stop kill it.
        if self.plot_proc.is_alive():
            logger.warn('Terminating child proc...')
            self.plot_proc.terminate()
            self.plot_proc.join(timeout=0.3)

    def show_plots(self) -> None:
        plt.show(block=False)  # Make our plots appear.


def start_plot_proc(pm: PlotManager): ...
