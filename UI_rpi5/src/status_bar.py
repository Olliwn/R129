"""
R129 Driver UI -- Status Bar
Compact top strip showing page heading, clock, LTE status, and active warnings.
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

    def __init__(self, state: VehicleState, modem=None, parent=None):
        super().__init__(parent)
        self._state = state
        self._modem = modem
        self._page_name = "HOME"
        self.setFixedHeight(self.HEIGHT)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(1000)

        if modem:
            modem.state_changed.connect(self.update)

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

        draw_dot_text(p, margin, y, self._page_name, on_color=theme.AMBER)

        ts = time.strftime("%H:%M")
        tw = dot_text_width(ts)
        draw_dot_text(p, w - tw - margin, y, ts, on_color=theme.TICK_WHITE)

        lte_gap = 30
        lte_w = self._draw_lte(p, w - tw - margin - lte_gap, y)

        vals = self._state.snapshot()
        warnings = []
        if vals["coolant"] > 110:
            warnings.append("COOL!")
        if vals["voltage"] < 11.5:
            warnings.append("BATT!")
        if vals["oil_temp"] > 130:
            warnings.append("OIL!")

        center_right = w - tw - margin - lte_w - 24
        if warnings:
            warn_str = "  ".join(warnings)
            ww = dot_text_width(warn_str)
            cx = max(dot_text_width(self._page_name) + margin + 20,
                     (margin + center_right - ww) / 2)
            draw_dot_text(p, cx, y, warn_str, on_color=theme.NEEDLE_RED)
        else:
            info = f"{vals['voltage']:.1f}V  {vals['coolant']:.0f}C"
            iw = dot_text_width(info)
            cx = max(dot_text_width(self._page_name) + margin + 20,
                     (margin + center_right - iw) / 2)
            draw_dot_text(p, cx, y, info, on_color=theme.AMBER)

        p.end()

    def _draw_lte(self, p: QPainter, right_x: float, y: float) -> float:
        """Draw LTE indicator left of clock. Returns total width consumed."""
        if not self._modem:
            return 0

        m = self._modem
        sc = theme.DOT_SCALE

        if not m.enabled:
            txt = "LTE OFF"
            tw = dot_text_width(txt)
            draw_dot_text(p, right_x - tw, y, txt, on_color=theme.AMBER_DARK)
            return tw + 8

        bars = m.rssi_bars
        registered = m.registered

        bar_w = 4 * sc
        bar_gap = 2 * sc
        bar_count = 4
        total_bars_w = bar_count * bar_w + (bar_count - 1) * bar_gap
        bar_base_y = y + 7 * 5 * sc
        max_bar_h = 6 * 5 * sc

        bar_start_x = right_x - total_bars_w

        for i in range(bar_count):
            bx = bar_start_x + i * (bar_w + bar_gap)
            frac = (i + 1) / bar_count
            bh = max_bar_h * frac
            by = bar_base_y - bh

            if i < bars and registered:
                color = theme.GREEN
            elif registered:
                color = theme.AMBER_DARK
            else:
                color = QColor(80, 20, 10)

            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.drawRect(QRectF(bx, by, bar_w, bh))

        label = "LTE"
        lw = dot_text_width(label)
        label_x = bar_start_x - lw - 6 * sc

        if registered:
            label_color = theme.GREEN
        elif m.error:
            label_color = theme.NEEDLE_RED
        else:
            label_color = theme.AMBER_DIM

        draw_dot_text(p, label_x, y, label, on_color=label_color)

        return right_x - label_x + 8
