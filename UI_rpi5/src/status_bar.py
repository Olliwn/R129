"""
R129 Driver UI -- Status Bar
Compact top strip showing page heading, clock, and active warnings.
Rendered in dot-matrix style to match the overall retro aesthetic.
All colors bright enough for daylight readability.
"""

import time

from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor

import theme
from dot_matrix import draw_dot_text, dot_line_height, dot_text_width
from vehicle_state import VehicleState


class StatusBar(QWidget):
    HEIGHT = 62

    def __init__(self, state: VehicleState, parent=None):
        super().__init__(parent)
        self._state = state
        self._page_name = "HOME"
        self.setFixedHeight(self.HEIGHT)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(1000)

    def set_page_name(self, name: str):
        if self._page_name != name:
            self._page_name = name
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), theme.BG)

        p.setPen(QPen(theme.SIDEBAR_SEPARATOR, 1))
        p.drawLine(0, h - 1, w, h - 1)

        y = 6
        margin = 12

        # page heading (left) -- full amber
        draw_dot_text(p, margin, y, self._page_name, on_color=theme.AMBER)

        # clock (right) -- bright warm white
        ts = time.strftime("%H:%M")
        tw = dot_text_width(ts)
        draw_dot_text(p, w - tw - margin, y, ts, on_color=theme.TICK_WHITE)

        # warnings / info in center
        vals = self._state.snapshot()
        warnings = []
        if vals["coolant"] > 110:
            warnings.append("COOL!")
        if vals["voltage"] < 11.5:
            warnings.append("BATT!")
        if vals["oil_temp"] > 130:
            warnings.append("OIL!")

        if warnings:
            warn_str = "  ".join(warnings)
            ww = dot_text_width(warn_str)
            draw_dot_text(p, (w - ww) / 2, y, warn_str, on_color=theme.NEEDLE_RED)
        else:
            info = f"{vals['voltage']:.1f}V  {vals['coolant']:.0f}C"
            iw = dot_text_width(info)
            draw_dot_text(p, (w - iw) / 2, y, info, on_color=theme.AMBER)

        p.end()
