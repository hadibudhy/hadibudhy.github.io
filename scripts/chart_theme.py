"""Shared style tokens for the portfolio's static charts."""

from __future__ import annotations

import matplotlib as mpl
from matplotlib.axes import Axes
from matplotlib.figure import Figure

CANVAS = "#FAFAF8"
PAPER = "#FFFFFF"
INK = "#202B30"
MUTED = "#52636B"
BORDER = "#C9D3D8"
GRID = "#E3E9EC"
ACCENT = "#225B73"
SECONDARY = "#64867E"
HIGHLIGHT = "#B45435"
WARNING = "#94632C"
PANEL = "#F1F4F5"
OBSERVED_FILL = "#E8F0ED"
WARNING_FILL = "#F5EEE7"
FONT = "Arial"

FIGSIZE = (12, 6.75)
WIDE_SIZE = FIGSIZE
DPI = 160

mpl.rcParams.update({
    "font.family": FONT,
    "font.size": 10,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "text.color": INK,
    "figure.facecolor": CANVAS,
    "savefig.facecolor": CANVAS,
})


def style_figure(figure: Figure) -> None:
    figure.patch.set_facecolor(CANVAS)


def style_axis(axis: Axes, grid_axis: str = "y") -> None:
    axis.set_facecolor(CANVAS)
    axis.set_axisbelow(True)
    axis.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    axis.tick_params(axis="both", colors=MUTED, labelsize=10, length=3, width=0.8)
    axis.xaxis.label.set_color(MUTED)
    axis.yaxis.label.set_color(MUTED)
    for side in ("top", "right"):
        axis.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        axis.spines[side].set_color(BORDER)
        axis.spines[side].set_linewidth(0.8)


def add_header(figure: Figure, title: str, subtitle: str) -> None:
    figure.text(0.065, 0.955, title, ha="left", va="top", color=INK,
                fontsize=19, fontweight="bold", fontfamily=FONT)
    figure.text(0.065, 0.895, subtitle, ha="left", va="top", color=MUTED,
                fontsize=10.5, fontfamily=FONT)


def add_source(figure: Figure, source: str) -> None:
    figure.text(0.065, 0.025, f"Source: {source}", ha="left", va="bottom",
                color=MUTED, fontsize=8.5, fontfamily=FONT)
