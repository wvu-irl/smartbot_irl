from time import time, sleep
from typing import List
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from smartbot_irl.data import LaserScan, Frame, State, timestamp

import threading
import matplotlib.pyplot as plt
import matplotlib

# matplotlib.use("TkAgg")
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec


class BasePlot:
    """Base class for custom student plots."""

    def init(self, ax):
        raise NotImplementedError

    def update(self, df):
        raise NotImplementedError


class SimplePlot(BasePlot):
    def __init__(self, x, y, kind, kwargs=None):
        self.x = x
        self.y = y
        self.kind = kind
        self.kwargs = kwargs or {}
        self.artist = None
        self.ax = None

        # Sliding windows
        self.x_window = self.kwargs.pop("x_window", None)  # float seconds or units
        self.y_window = self.kwargs.pop("y_window", None)  # float units
        self.equal_aspect = self.kwargs.pop("equal_aspect", False)

    def init(self, ax):
        self.ax = ax

        # Extract label/title/xlabel/ylabel from kwargs.
        self.title = self.kwargs.pop("title", None)
        self.xlabel = self.kwargs.pop("xlabel", None)
        self.ylabel = self.kwargs.pop("ylabel", None)

        if self.kind == "line":
            (self.artist,) = ax.plot([], [], **self.kwargs)
        elif self.kind == "step":
            (self.artist,) = ax.step([], [], **self.kwargs)
        elif self.kind == "scatter":
            self.artist = ax.scatter([], [], **self.kwargs)
        else:
            raise ValueError(f"Unknown plot type: {self.kind}")

        if self.title:
            ax.set_title(self.title)
        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)

    def update(self, df):
        # Skip if columns do not exist
        if self.x not in df.columns or self.y not in df.columns:
            return
        rows = df[[self.x, self.y]].dropna()
        if rows.empty:
            return

        if not hasattr(self, "_frame_count"):
            self._frame_count = 0
        self._frame_count += 1

        # Skip updating the artwork 2 out of every 3 frames
        do_update = self._frame_count % 1 == 0

        # Only rescale axes every 10 frames
        do_rescale = self._frame_count % 1 == 0

        xs = rows[self.x].values
        ys = rows[self.y].values

        # -------------------------------------
        # Downsample if too many points
        # -------------------------------------
        if len(xs) > 200:
            xs = xs[::5]
            ys = ys[::5]

        # Convert booleans to integers for scaling & plotting
        if ys.dtype == bool:
            ys = ys.astype(int)

        if xs.dtype == bool:
            xs = xs.astype(int)
            # -------------------------------------
        # Update artists (but throttled)
        # -------------------------------------
        if do_update:
            if self.kind in ("line", "step"):
                self.artist.set_data(xs, ys)
            else:
                self.artist.set_offsets(np.column_stack([xs, ys]))
        if do_rescale:
            xmin, xmax = xs.min(), xs.max()
            ymin, ymax = ys.min(), ys.max()
            span = max(xmax - xmin, ymax - ymin)

            if span == 0:
                span = 1e-3
            pad = span * 0.05

            self.ax.set_xlim(xmin - pad, xmin + span + pad)
            self.ax.set_ylim(ymin - pad, ymin + span + pad)

            if self.equal_aspect:
                self.ax.set_aspect("equal", adjustable="box")
            else:
                self.ax.set_aspect("auto")

            if self.x_window is not None:
                xmax = xs.max()
                xmin = xmax - self.x_window
                self.ax.set_xlim(xmin, xmax)

            else:
                # Autoscale X if no sliding window
                xmin, xmax = xs.min(), xs.max()
                if xmin == xmax:
                    xmax = xmin + 1e-3
                pad = (xmax - xmin) * 0.05
                self.ax.set_xlim(xmin - pad, xmax + pad)

            if self.y_window is not None:
                ymax = ys.max()
                ymin = ymax - self.y_window
                self.ax.set_ylim(ymin, ymax)

            else:
                # Autoscale Y if no sliding window.
                ymin, ymax = ys.min(), ys.max()
                if ymin == ymax:
                    ymax = ymin + 1e-3
                pad = (ymax - ymin) * 0.05
                self.ax.set_ylim(ymin - pad, ymax + pad)

            # Maintain square aspect for scatters.
            if self.kind == "scatter":
                self.ax.set_aspect("equal", adjustable="box")


class LivePlotter:
    def __init__(self, state: State, plot_specs: List):
        """
        plot_specs may be:
            - flat list for a single window
            - list of lists for multiple windows
        """
        self.state = state
        self.windows = []

        # Normalize to list-of-lists
        if len(plot_specs) > 0 and isinstance(plot_specs[0], tuple):
            plot_specs = [plot_specs]  # Make single item list.

        for win_specs in plot_specs:
            plots = []
            for spec in win_specs:
                if isinstance(spec, BasePlot):
                    plots.append(spec)
                elif isinstance(spec, tuple):
                    if len(spec) == 3:
                        x, y, kind = spec
                        plots.append(SimplePlot(x, y, kind))
                    elif len(spec) == 4:
                        x, y, kind, kwargs = spec
                        plots.append(SimplePlot(x, y, kind, kwargs))
                    else:
                        raise ValueError("Bad plot spec tuple")
                else:
                    raise TypeError("Plot spec must be BasePlot or tuple")
            self.windows.append(plots)

        # Create all windows
        self._create_windows()

    def _create_windows(self):
        self.figures = []
        self.axes = []

        for plots in self.windows:
            # fig, axs = plt.subplots(len(plots), 1, figsize=(6, 3 * len(plots)))
            fig, axs = plt.subplots(
                len(plots),
                1,
                figsize=(6, 3 * len(plots)),
                constrained_layout=True,
            )

            if len(plots) == 1:
                axs = [axs]

            for ax, plot in zip(axs, plots):
                plot.init(ax)

            self.figures.append(fig)
            self.axes.append(axs)

        plt.ion()
        plt.show()

    # def update(self):
    #     df = self.state.state_vec
    #     if df.empty:
    #         return

    #     # Limit df to last 2000 rows to prevent performance collapse
    #     if len(df) > 2000:
    #         df = df.tail(2000)

    #     for plots, fig, axs in zip(self.windows, self.figures, self.axes):
    #         # -------------------------------------------------
    #         # 1. Get the proper Tk widget for this figure
    #         # -------------------------------------------------
    #         tk_widget = fig.canvas.get_tk_widget()

    #         # -------------------------------------------------
    #         # 2. SAFELY cancel all pending Tk "after" callbacks
    #         # -------------------------------------------------
    #         try:
    #             afters = tk_widget.after_info()  # returns tuple of callback IDs
    #             for aid in afters:
    #                 try:
    #                     tk_widget.after_cancel(aid)
    #                 except Exception:
    #                     pass
    #         except Exception:
    #             pass  # after_info not available on some backends

    #         # -------------------------------------------------
    #         # 3. Your original high-speed blitting logic
    #         # -------------------------------------------------
    #         for ax, plot in zip(axs, plots):
    #             plot.update(df)
    #             ax.draw_artist(ax.patch)
    #             ax.draw_artist(plot.artist)

    #         fig.canvas.blit(fig.bbox)
    #         fig.canvas.flush_events()

    def update(self):
        df = self.state.state_vec
        if df.empty:
            return
        # Limit df to last 2000 rows to prevent performance collapse
        if len(df) > 50:
            df = df.tail(50)

        # for plots, fig, axs in zip(self.windows, self.figures, self.axes):
        #     # Redraw only artists
        #     for ax, plot in zip(axs, plots):
        #         plot.update(df)
        #         ax.draw_artist(ax.patch)
        #         ax.draw_artist(plot.artist)

        #     # Blit onto the figure once
        #     fig.canvas.blit(fig.bbox)

        # # Required for Tk event loop, but cheap
        # fig.canvas.flush_events()

        for plots, fig in zip(self.windows, self.figures):
            for plot in plots:
                plot.update(df)
            fig.canvas.draw_idle()
            # fig.canvas.draw()
            # fig.canvas.flush_events()

        plt.pause(0.001)
        # fig.canvas.flush_events()


class FigureWrapper:
    def __init__(self, max_fps=20, **kwargs):
        self.fig = plt.figure()
        self.axes = []

        self._title = kwargs.pop("title", None)  # store it
        if self._title:
            self.fig.suptitle(self._title)

        self._fig_kwargs = kwargs
        self._apply_fig_kwargs()
        self.items = []  # (kind, artist, x_col, y_col)
        self.last_draw = 0
        self.min_dt = 1.0 / max_fps

    # def _new_subplot(self):
    #     """Add a new subplot row and rebuild layout cleanly."""
    #     n = len(self.axes) + 1
    #     self.fig.clear()

    #     gs = GridSpec(n, 1, figure=self.fig)
    #     new_axes = []

    #     # recreate existing empty axes
    #     for i in range(len(self.axes)):
    #         ax_new = self.fig.add_subplot(gs[i, 0])
    #         new_axes.append(ax_new)

    #     # create the new one
    #     ax_new = self.fig.add_subplot(gs[n - 1, 0])
    #     new_axes.append(ax_new)

    #     self.axes = new_axes
    #     return ax_new

    def _apply_fig_kwargs(self):
        """Applies kwargs to figure if figure has matching set_* methods."""
        for k, v in self._fig_kwargs.items():
            setter = f"set_{k}"
            if hasattr(self.fig, setter):
                getattr(self.fig, setter)(v)
            else:
                raise ValueError(f"{self.fig} does not accept figure kwarg '{k}'")

    from matplotlib.gridspec import GridSpec

    def _new_subplot(self):
        n = len(self.axes) + 1

        # Build a new gridspec with n rows
        gs = GridSpec(n, 1, figure=self.fig)

        # Reassign ALL EXISTING axes to their correct grid position
        for i, ax in enumerate(self.axes):
            ax.set_subplotspec(gs[i, 0])
            ax.set_position(gs[i, 0].get_position(self.fig))

        # Create and place the new axis
        ax_new = self.fig.add_subplot(gs[n - 1, 0])
        self.axes.append(ax_new)

        return ax_new

    # def _new_subplot(self):
    #     n = len(self.axes) + 1

    #     # clear figure and rebuild
    #     self.fig.clear()
    #     self._apply_fig_kwargs()
    #     if self._title:
    #         self.fig.suptitle(self._title)

    #     gs = GridSpec(n, 1, figure=self.fig)

    #     new_axes = []

    #     # recreate old axes
    #     for i, old_ax in enumerate(self.axes):
    #         ax_new = self.fig.add_subplot(gs[i, 0])

    #         # migrate artists (lines, scatters, legends)
    #         for artist in old_ax.get_children():
    #             try:
    #                 artist.remove()
    #                 ax_new.add_artist(artist)
    #             except Exception:
    #                 pass

    #         new_axes.append(ax_new)

    #     # create new axis
    #     ax_new = self.fig.add_subplot(gs[n - 1, 0])
    #     new_axes.append(ax_new)

    #     self.axes = new_axes
    #     return ax_new

    # def _new_subplot(self):
    #     n = len(self.axes) + 1

    #     gs = GridSpec(n, 1, figure=self.fig)
    #     new_axes = []

    #     # reparent all existing axes into new grid positions
    #     for i, old_ax in enumerate(self.axes):
    #         # move old axes into new GridSpec cell
    #         new_pos = gs[i, 0]
    #         old_ax.set_subplotspec(new_pos)
    #         new_axes.append(old_ax)

    #     # create the new one
    #     ax_new = self.fig.add_subplot(gs[n - 1, 0])
    #     new_axes.append(ax_new)

    #     self.axes = new_axes
    #     return ax_new

    # def _new_subplot(self):
    #     n = len(self.axes) + 1
    #     self.fig.clear()

    #     # reapply stored fig kwargs (same behavior as axes kwargs)
    #     self._apply_fig_kwargs()

    #     # reapply title
    #     if self._title:
    #         self.fig.suptitle(self._title)

    #     gs = GridSpec(n, 1, figure=self.fig)
    #     new_axes = []

    #     for i in range(len(self.axes)):
    #         ax_new = self.fig.add_subplot(gs[i, 0])
    #         new_axes.append(ax_new)

    #     ax_new = self.fig.add_subplot(gs[n - 1, 0])
    #     new_axes.append(ax_new)

    #     self.axes = new_axes
    #     return ax_new

    def _apply_kwargs(self, target, kwargs):
        """Applies kwargs to target if target has a matching set_* method."""
        for k, v in kwargs.items():
            setter = f"set_{k}"
            if hasattr(target, setter):
                getattr(target, setter)(v)
            else:
                raise ValueError(f"{target} does not accept kwarg '{k}'")

    def add_line(self, x_col=None, y_col=None, window=1000, **kwargs):
        if y_col is None:
            raise ValueError("y_col must be specified")

        # Always create a new subplot
        ax = self._new_subplot()

        # Normalize y_col to a list
        if not isinstance(y_col, list):
            y_col_list = [y_col]
        else:
            y_col_list = y_col

        # Split kwargs into artist kwargs vs axes kwargs
        artist_kwargs = {}
        axes_kwargs = {}

        for k, v in kwargs.items():
            setter = f"set_{k}"
            if hasattr(ax, setter):
                axes_kwargs[k] = v
            else:
                artist_kwargs[k] = v

        # Get legend labels.
        # # labels = artist_kwargs.pop("label", None)
        # if isinstance(labels, list):
        #     if len(labels) != len(y_col_list):
        #         raise ValueError("label list length must match y_col list")
        # else:
        #     labels = [labels] * len(y_col_list)

        # Extract label(s)
        raw_labels = artist_kwargs.pop("labels", None)

        if raw_labels is None:
            # No labels provided → auto-generate None for all
            labels = [None] * len(y_col_list)
        elif isinstance(raw_labels, list):
            if len(raw_labels) != len(y_col_list):
                raise ValueError("label list length must match y_col list")
            labels = raw_labels
        else:
            # broadcast single label
            labels = [raw_labels] * len(y_col_list)

        # Extract color(s)
        # color = artist_kwargs.pop("color", None)

        # if isinstance(color, list):
        #     if len(color) != len(y_col_list):
        #         raise ValueError("color list length must match y_col list")
        # else:
        #     # broadcast single color
        #     color = [color] * len(y_col_list)
        raw_color = artist_kwargs.pop("color", None)
        if isinstance(raw_color, list):
            if len(raw_color) != len(y_col_list):
                raise ValueError("color list length must match y_col list")
            colors = raw_color
        else:
            colors = [raw_color] * len(y_col_list)

        # artists = []
        # for i in range(len(y_col_list)):
        #     ak = dict(artist_kwargs)
        #     if color[i] is not None:
        #         ak["color"] = color[i]
        #     if labels[i] is not None:
        #         ak["label"] = labels[i]

        #     (line,) = ax.plot([], [], **ak)
        #     artists.append(line)
        artists = []
        for lbl, col in zip(labels, colors):
            ak = dict(artist_kwargs)
            if col is not None:
                ak["color"] = col
            if lbl is not None:
                ak["label"] = lbl

            (line,) = ax.plot([], [], **ak)
            artists.append(line)

        # # Create multiple Line2D artists if needed
        # artists = []
        # for _ in y_col_list:
        #     (line,) = ax.plot([], [], **artist_kwargs)
        #     artists.append(line)

        # Apply axes kwargs
        if axes_kwargs:
            self._apply_kwargs(ax, axes_kwargs)

        # If any line has a label, add a legend
        # if any(line.get_label() != "_nolegend_" for line in artists):
        #     ax.legend(handlelength=3)
        if any(lbl is not None for lbl in labels):
            ax.legend(handlelength=3)

        # For each y-col create its own buffer
        buffers = [([], []) for _ in y_col_list]
        self.fig.tight_layout()

        self.items.append((ax, "line", artists, x_col, y_col_list, window, buffers))
        return artists

    def add_scatter(self, x_col=None, y_col=None, window=1000, **kwargs):
        # For scatter, still create marker-style line2D objects
        kwargs.setdefault("ls", "")
        kwargs.setdefault("marker", "o")
        return self.add_line(x_col, y_col, window, **kwargs)

    def update(self, df_last_row: pd.Series):
        for ax, kind, artists, x_col, y_col_list, window, buffers in self.items:
            # Compute x value once
            if x_col is None:
                xval = df_last_row.name
            else:
                xval = df_last_row[x_col]

            # Update each y-column independently
            for line, ycol, (xbuf, ybuf) in zip(artists, y_col_list, buffers):
                yval = df_last_row[ycol]

                xbuf.append(xval)
                ybuf.append(yval)

                if len(xbuf) > window:
                    xbuf.pop(0)
                    ybuf.pop(0)

                line.set_data(xbuf, ybuf)

            ax.relim()
            ax.autoscale_view()

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
    def __init__(self):
        self.figures = []

    def add_figure(self, max_fps=60, **kwargs):
        fw = FigureWrapper(max_fps=max_fps, **kwargs)
        self.figures.append(fw)
        return fw

    def update_all(self, data):
        for fw in self.figures:
            fw.update(data)
            fw.redraw_if_needed()
