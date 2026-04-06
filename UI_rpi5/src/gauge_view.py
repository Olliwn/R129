"""
R129 Driver UI -- Modern Gauge Cluster View
3 circular gauges (RPM, speed, coolant) + 3 horizontal bars (oil, fuel, voltage).
Uses shared theme and improved rendering (tapered needles, bezel rings, shadows).
Gauge text uses gauge_font() (unscaled) to avoid overlap.
"""

import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import (
    QPainter, QPen, QBrush, QFontMetrics,
    QColor, QRadialGradient, QPolygonF,
)

import theme
from input_actions import InputAction
from vehicle_state import VehicleState


class GaugeView(QWidget):
    def __init__(self, state: VehicleState):
        super().__init__()
        self._state = state
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(33)

    def handle_input(self, action: InputAction) -> bool:
        return False

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), theme.BG)

        vals = self._state.snapshot()

        gauge_h = int(h * 0.72)
        tacho_r = int(gauge_h * 0.42)
        speedo_r = int(gauge_h * 0.46)
        coolant_r = int(gauge_h * 0.42)
        cy = int(h * 0.40)

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

        # Bars: proportional positioning
        bar_h = 18
        bar_w = int(w * 0.18)
        bar_y = h - bar_h - 50
        bar_gap = int(w * 0.04)
        bar_x1 = int(w * 0.05)
        bar_x2 = bar_x1 + bar_w + bar_gap
        bar_x3 = bar_x2 + bar_w + bar_gap

        self._draw_bar(p, bar_x1, bar_y, bar_w, bar_h, vals["oil_temp"], 40, 150, "OIL TEMP", "\u00b0C")
        self._draw_bar(p, bar_x2, bar_y, bar_w, bar_h, vals["fuel"], 0, 100, "FUEL", "%")
        self._draw_bar(p, bar_x3, bar_y, bar_w, bar_h, vals["voltage"], 10, 16, "VOLTAGE", "V")

        # ADS mode
        f = theme.gauge_font(12, bold=True)
        p.setFont(f)
        fm = QFontMetrics(f)
        mode = vals["ads_mode"]
        color = theme.NEEDLE_RED if mode == "SPORT" else theme.AMBER
        p.setPen(color)
        ads_text = f"ADS: {mode}"
        p.drawText(w - fm.horizontalAdvance(ads_text) - 20, bar_y + 12, ads_text)

        p.end()

    # ── Gauge ────────────────────────────────────────────────────────

    def _draw_gauge(self, p, cx, cy, radius, value, min_val, max_val,
                    label, unit, major_ticks, redline_start=None,
                    start_angle=225, sweep=270):

        grad = QRadialGradient(cx, cy, radius + 6)
        grad.setColorAt(0.90, theme.BEZEL_DARK)
        grad.setColorAt(0.95, theme.BEZEL_HIGHLIGHT)
        grad.setColorAt(1.00, theme.BEZEL_DARK)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(grad))
        p.drawEllipse(QPointF(cx, cy), radius + 6, radius + 6)

        p.setBrush(QBrush(theme.GAUGE_FACE))
        p.drawEllipse(QPointF(cx, cy), radius, radius)

        if redline_start is not None:
            s_frac = (redline_start - min_val) / (max_val - min_val)
            arc_start = start_angle - s_frac * sweep
            arc_end = start_angle - sweep
            pen = QPen(theme.NEEDLE_RED, 3)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            rect = QRectF(cx - (radius - 8), cy - (radius - 8),
                          (radius - 8) * 2, (radius - 8) * 2)
            p.drawArc(rect, int(arc_end * 16), int((arc_start - arc_end) * 16))

        for i, tick_val in enumerate(major_ticks):
            frac = (tick_val - min_val) / (max_val - min_val)
            angle_deg = start_angle - frac * sweep
            angle = math.radians(angle_deg)
            in_red = redline_start is not None and tick_val >= redline_start
            color = theme.NEEDLE_RED if in_red else theme.TICK_WHITE

            r_outer = radius - 6
            r_inner = radius - 22
            p.setPen(QPen(color, 2))
            p.drawLine(
                QPointF(cx + r_inner * math.cos(angle), cy - r_inner * math.sin(angle)),
                QPointF(cx + r_outer * math.cos(angle), cy - r_outer * math.sin(angle)),
            )

            font_size = max(8, radius // 18)
            tf = theme.gauge_font(font_size)
            p.setFont(tf)
            p.setPen(color)
            tick_label = str(int(tick_val))
            fm = QFontMetrics(tf)
            r_text = radius - 34
            tx = cx + r_text * math.cos(angle) - fm.horizontalAdvance(tick_label) / 2
            ty = cy - r_text * math.sin(angle) + fm.ascent() / 2
            p.drawText(QPointF(tx, ty), tick_label)

            if i < len(major_ticks) - 1:
                next_val = major_ticks[i + 1]
                for m in range(1, 5):
                    mval = tick_val + m * (next_val - tick_val) / 5
                    mfrac = (mval - min_val) / (max_val - min_val)
                    mangle = math.radians(start_angle - mfrac * sweep)
                    in_red_m = redline_start is not None and mval >= redline_start
                    mc = theme.NEEDLE_RED if in_red_m else theme.TICK_DIM
                    p.setPen(QPen(mc, 1))
                    p.drawLine(
                        QPointF(cx + (radius - 14) * math.cos(mangle),
                                cy - (radius - 14) * math.sin(mangle)),
                        QPointF(cx + (radius - 6) * math.cos(mangle),
                                cy - (radius - 6) * math.sin(mangle)),
                    )

        lf = theme.gauge_font(max(9, radius // 16), bold=True)
        p.setFont(lf)
        p.setPen(theme.TICK_DIM)
        fm = QFontMetrics(lf)
        p.drawText(QPointF(cx - fm.horizontalAdvance(label) / 2, cy + radius * 0.20), label)
        if unit:
            uf = theme.gauge_font(max(7, radius // 20))
            p.setFont(uf)
            ufm = QFontMetrics(uf)
            p.drawText(QPointF(cx - ufm.horizontalAdvance(unit) / 2, cy + radius * 0.34), unit)

        val_frac = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        needle_angle_deg = start_angle - val_frac * sweep
        needle_angle = math.radians(needle_angle_deg)
        perp = needle_angle + math.pi / 2
        tip_len = radius - 24
        tail_len = radius * 0.15
        half_base = 2.5
        half_tip = 0.5

        tip = QPointF(cx + tip_len * math.cos(needle_angle),
                       cy - tip_len * math.sin(needle_angle))
        tail = QPointF(cx - tail_len * math.cos(needle_angle),
                        cy + tail_len * math.sin(needle_angle))
        bl = QPointF(cx + half_base * math.cos(perp), cy - half_base * math.sin(perp))
        br = QPointF(cx - half_base * math.cos(perp), cy + half_base * math.sin(perp))
        tl = QPointF(tip.x() + half_tip * math.cos(perp),
                      tip.y() - half_tip * math.sin(perp))
        tr = QPointF(tip.x() - half_tip * math.cos(perp),
                      tip.y() + half_tip * math.sin(perp))

        needle_poly = QPolygonF([tail, bl, tl, tr, br])

        shadow_poly = QPolygonF()
        for pt in needle_poly:
            shadow_poly.append(QPointF(pt.x() + 2, pt.y() + 2))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(0, 0, 0, 100)))
        p.drawPolygon(shadow_poly)

        p.setBrush(QBrush(theme.NEEDLE_AMBER))
        p.setPen(QPen(QColor(180, 110, 20), 0.5))
        p.drawPolygon(needle_poly)

        hub_grad = QRadialGradient(cx - 1, cy - 1, 8)
        hub_grad.setColorAt(0.0, QColor(120, 115, 105))
        hub_grad.setColorAt(0.6, QColor(70, 68, 62))
        hub_grad.setColorAt(1.0, QColor(40, 38, 34))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(hub_grad))
        p.drawEllipse(QPointF(cx, cy), 7, 7)

    # ── Bar gauge ────────────────────────────────────────────────────

    def _draw_bar(self, p, x, y, w, h, value, min_val, max_val, label, unit_str):
        p.setPen(QPen(theme.AMBER_DARK, 1))
        p.setBrush(Qt.NoBrush)
        p.drawRect(QRectF(x, y, w, h))

        fill_frac = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        fill_w = (w - 4) * fill_frac
        if fill_w > 0:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(theme.AMBER))
            p.drawRect(QRectF(x + 2, y + 2, fill_w, h - 4))

        f = theme.gauge_font(10, bold=True)
        p.setFont(f)
        fm = QFontMetrics(f)
        p.setPen(theme.AMBER_DIM)
        p.drawText(QPointF(x, y - 6), label)

        p.setPen(theme.AMBER)
        val_text = f"{int(value)} {unit_str}"
        p.drawText(QPointF(x + w - fm.horizontalAdvance(val_text), y - 6), val_text)
