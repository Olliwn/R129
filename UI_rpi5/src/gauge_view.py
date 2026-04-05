"""
R129 Driver UI -- Gauge Cluster View
Classic Mercedes-Benz VDO style: dark background, amber dials.
Rendered with QPainter for hardware-accelerated antialiased drawing.
"""

import math
import time

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics, QBrush

BG = QColor(5, 5, 8)
AMBER = QColor(255, 160, 30)
AMBER_DIM = QColor(140, 80, 10)
AMBER_DARK = QColor(60, 35, 5)
NEEDLE_RED = QColor(200, 40, 30)
BEZEL = QColor(30, 28, 25)


class GaugeView(QWidget):
    def __init__(self):
        super().__init__()
        self.t0 = time.monotonic()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(33)  # ~30 fps

    def _simulated_values(self):
        """Generate slowly oscillating demo values."""
        t = time.monotonic() - self.t0
        return {
            "rpm": 800 + 400 * math.sin(t * 0.3) + 200 * math.sin(t * 0.7),
            "speed": 60 + 30 * math.sin(t * 0.2) + 10 * math.sin(t * 0.5),
            "coolant": 85 + 5 * math.sin(t * 0.15),
            "oil_temp": 90 + 8 * math.sin(t * 0.1),
            "fuel": 65 + 10 * math.sin(t * 0.05),
            "voltage": 13.8 + 0.3 * math.sin(t * 0.4),
            "ads_mode": "SPORT" if int(t) % 10 < 5 else "COMFORT",
        }

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        w, h = self.width(), self.height()

        p.fillRect(self.rect(), BG)

        vals = self._simulated_values()

        self._draw_title_bar(p, w)

        tacho_r = int(h * 0.30)
        speedo_r = int(h * 0.33)
        coolant_r = int(h * 0.30)
        cy = h // 2 + 20

        self._draw_gauge(
            p, int(w * 0.20), cy, tacho_r,
            vals["rpm"] / 1000, 0, 7,
            "RPM", "\u00d71000",
            [0, 1, 2, 3, 4, 5, 6, 7],
            redline_start=6.2,
        )
        self._draw_gauge(
            p, w // 2, cy, speedo_r,
            vals["speed"], 0, 260,
            "km/h", "",
            list(range(0, 280, 20)),
        )
        self._draw_gauge(
            p, int(w * 0.80), cy, coolant_r,
            vals["coolant"], 40, 130,
            "COOLANT", "\u00b0C",
            [40, 60, 80, 100, 120, 130],
            redline_start=110,
        )

        bar_y = h - 70
        self._draw_bar(p, 60, bar_y, 250, 18, vals["oil_temp"], 40, 150, "OIL TEMP", "\u00b0C")
        self._draw_bar(p, 380, bar_y, 250, 18, vals["fuel"], 0, 100, "FUEL", "%")
        self._draw_bar(p, w - 560, bar_y, 250, 18, vals["voltage"], 10, 16, "VOLTAGE", "V")

        ads_font = QFont("Sans", 11, QFont.Bold)
        p.setFont(ads_font)
        mode = vals["ads_mode"]
        color = NEEDLE_RED if mode == "SPORT" else AMBER
        p.setPen(color)
        p.drawText(w - 120, bar_y + 14, f"ADS: {mode}")

        p.end()

    def _draw_title_bar(self, p, w):
        title_font = QFont("Sans", 13, QFont.Bold)
        p.setFont(title_font)
        p.setPen(AMBER_DIM)
        title = "R129  \u00b7  500 SL  \u00b7  AOK912"
        fm = QFontMetrics(title_font)
        tw = fm.horizontalAdvance(title)
        p.drawText((w - tw) // 2, 26, title)

        small_font = QFont("Sans", 10)
        p.setFont(small_font)
        p.setPen(AMBER_DARK)
        ts = time.strftime("%H:%M")
        p.drawText(w - 60, 26, ts)

    def _draw_gauge(self, p, cx, cy, radius, value, min_val, max_val,
                    label, unit, major_ticks, redline_start=None,
                    start_angle=225, sweep=270):
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(BEZEL))
        p.drawEllipse(QPointF(cx, cy), radius + 4, radius + 4)

        p.setBrush(QBrush(QColor(12, 12, 15)))
        p.drawEllipse(QPointF(cx, cy), radius, radius)

        p.setPen(QPen(AMBER_DARK, 2))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(cx, cy), radius, radius)

        for i, tick_val in enumerate(major_ticks):
            frac = (tick_val - min_val) / (max_val - min_val)
            angle_deg = start_angle - frac * sweep
            angle = math.radians(angle_deg)

            in_redline = redline_start is not None and tick_val >= redline_start
            color = NEEDLE_RED if in_redline else AMBER

            r_outer = radius - 8
            r_inner = radius - 28
            x0 = cx + r_inner * math.cos(angle)
            y0 = cy - r_inner * math.sin(angle)
            x1 = cx + r_outer * math.cos(angle)
            y1 = cy - r_outer * math.sin(angle)
            p.setPen(QPen(color, 3))
            p.drawLine(QPointF(x0, y0), QPointF(x1, y1))

            font_size = max(9, radius // 16)
            tick_font = QFont("Sans", font_size)
            p.setFont(tick_font)
            p.setPen(color)
            tick_label = str(int(tick_val))
            fm = QFontMetrics(tick_font)
            r_text = radius - 40
            tx = cx + r_text * math.cos(angle) - fm.horizontalAdvance(tick_label) / 2
            ty = cy - r_text * math.sin(angle) + fm.ascent() / 2
            p.drawText(QPointF(tx, ty), tick_label)

            if i < len(major_ticks) - 1:
                next_val = major_ticks[i + 1]
                for m in range(1, 5):
                    mval = tick_val + m * (next_val - tick_val) / 5
                    mfrac = (mval - min_val) / (max_val - min_val)
                    mangle = math.radians(start_angle - mfrac * sweep)
                    mr_outer = radius - 8
                    mr_inner = radius - 18
                    mx0 = cx + mr_inner * math.cos(mangle)
                    my0 = cy - mr_inner * math.sin(mangle)
                    mx1 = cx + mr_outer * math.cos(mangle)
                    my1 = cy - mr_outer * math.sin(mangle)
                    in_red_m = redline_start is not None and mval >= redline_start
                    p.setPen(QPen(NEEDLE_RED if in_red_m else AMBER_DARK, 1))
                    p.drawLine(QPointF(mx0, my0), QPointF(mx1, my1))

        label_font = QFont("Sans", max(10, radius // 14), QFont.Bold)
        p.setFont(label_font)
        p.setPen(AMBER_DIM)
        fm = QFontMetrics(label_font)
        p.drawText(QPointF(cx - fm.horizontalAdvance(label) / 2, cy + radius * 0.22), label)

        unit_font = QFont("Sans", max(8, radius // 18))
        p.setFont(unit_font)
        p.setPen(AMBER_DARK)
        fm = QFontMetrics(unit_font)
        p.drawText(QPointF(cx - fm.horizontalAdvance(unit) / 2, cy + radius * 0.38), unit)

        val_frac = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        needle_angle = math.radians(start_angle - val_frac * sweep)
        needle_len = radius - 30
        nx = cx + needle_len * math.cos(needle_angle)
        ny = cy - needle_len * math.sin(needle_angle)
        tail_len = radius * 0.15
        tail_x = cx - tail_len * math.cos(needle_angle)
        tail_y = cy + tail_len * math.sin(needle_angle)
        p.setPen(QPen(AMBER, 3))
        p.drawLine(QPointF(tail_x, tail_y), QPointF(nx, ny))

        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(AMBER))
        p.drawEllipse(QPointF(cx, cy), 8, 8)
        p.setBrush(QBrush(BG))
        p.drawEllipse(QPointF(cx, cy), 5, 5)

    def _draw_bar(self, p, x, y, w, h, value, min_val, max_val, label, unit_str):
        p.setPen(QPen(AMBER_DARK, 1))
        p.setBrush(Qt.NoBrush)
        p.drawRect(QRectF(x, y, w, h))

        fill_frac = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        fill_w = (w - 4) * fill_frac
        if fill_w > 0:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(AMBER))
            p.drawRect(QRectF(x + 2, y + 2, fill_w, h - 4))

        font = QFont("Sans", 10, QFont.Bold)
        p.setFont(font)
        p.setPen(AMBER_DIM)
        p.drawText(QPointF(x, y - 6), label)

        p.setPen(AMBER)
        val_text = f"{int(value)} {unit_str}"
        fm = QFontMetrics(font)
        p.drawText(QPointF(x + w - fm.horizontalAdvance(val_text), y - 6), val_text)
