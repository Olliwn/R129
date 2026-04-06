"""
R129 Driver UI -- Classic Cluster View
Factory-faithful 5-gauge R129 instrument cluster.
Matches the night-illuminated reference: white markings, amber tapered needles,
charcoal gauge faces, chrome bezel rings, warning light strip.

Layout (left to right):
  1. Fuel / Coolant combo gauge (small)
  2. Oil temperature (small)
  3. Speedometer (large, center)
  4. Tachometer (medium-large)
  5. Analog clock (small)
"""

import math
import time

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import (
    QPainter, QPen, QBrush, QFont, QFontMetrics,
    QColor, QRadialGradient, QPolygonF, QConicalGradient,
)

import theme
from input_actions import InputAction
from vehicle_state import VehicleState


class ClassicClusterView(QWidget):
    def __init__(self, state: VehicleState):
        super().__init__()
        self._state = state
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(33)

    def handle_input(self, action: InputAction) -> bool:
        return False

    # ── Main paint ────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), theme.BG)

        vals = self._state.snapshot()

        cy_main = int(h * 0.46)
        cy_side = int(h * 0.48)

        speedo_r = int(h * 0.38)
        tacho_r = int(h * 0.30)
        small_r = int(h * 0.22)

        # 1. Fuel / Coolant combo (left)
        self._draw_combo_gauge(
            p, int(w * 0.11), cy_side, small_r,
            vals["fuel"], 0, 100, "1/1", "0", "F",
            vals["coolant"], 40, 130, "\u00b0C", "40", "130",
            redline_right=110,
        )

        # 2. Oil temperature (left-center)
        self._draw_gauge(
            p, int(w * 0.28), cy_side, small_r,
            vals["oil_temp"], 40, 150,
            "OIL", "\u00b0C",
            [40, 60, 80, 100, 120, 140],
            redline_start=130,
        )

        # 3. Speedometer (center, largest)
        self._draw_gauge(
            p, int(w * 0.50), cy_main, speedo_r,
            vals["speed"], 0, 260,
            "km/h", "",
            list(range(0, 280, 20)),
        )

        # 4. Tachometer (right-center)
        self._draw_gauge(
            p, int(w * 0.73), cy_side, tacho_r,
            vals["rpm"] / 1000, 0, 7,
            "RPM", "\u00d71000",
            [0, 1, 2, 3, 4, 5, 6, 7],
            redline_start=6.2,
        )

        # 5. Analog clock (right)
        self._draw_clock(p, int(w * 0.90), cy_side, small_r)

        # Warning lights strip
        self._draw_warning_strip(p, w, h, vals)

        p.end()

    # ── Gauge rendering ──────────────────────────────────────────────

    def _draw_gauge(self, p, cx, cy, radius, value, min_val, max_val,
                    label, unit, major_ticks, redline_start=None,
                    start_angle=225, sweep=270):

        self._draw_bezel(p, cx, cy, radius)
        self._draw_face(p, cx, cy, radius)

        # Redline arc
        if redline_start is not None:
            self._draw_redline_arc(
                p, cx, cy, radius, min_val, max_val,
                redline_start, max_val, start_angle, sweep,
            )

        # Ticks and labels
        for i, tick_val in enumerate(major_ticks):
            frac = (tick_val - min_val) / (max_val - min_val)
            angle_deg = start_angle - frac * sweep
            angle = math.radians(angle_deg)
            in_red = redline_start is not None and tick_val >= redline_start
            color = theme.NEEDLE_RED if in_red else theme.TICK_WHITE

            r_outer = radius - 6
            r_inner = radius - 22
            self._tick_line(p, cx, cy, r_inner, r_outer, angle, color, 2)

            font_size = max(8, radius // 18)
            self._tick_label(p, cx, cy, radius - 34, angle, str(int(tick_val)),
                             font_size, color)

            # Minor ticks
            if i < len(major_ticks) - 1:
                next_val = major_ticks[i + 1]
                for m in range(1, 5):
                    mval = tick_val + m * (next_val - tick_val) / 5
                    mfrac = (mval - min_val) / (max_val - min_val)
                    mangle = math.radians(start_angle - mfrac * sweep)
                    in_red_m = redline_start is not None and mval >= redline_start
                    mc = theme.NEEDLE_RED if in_red_m else theme.TICK_DIM
                    self._tick_line(p, cx, cy, radius - 14, radius - 6, mangle, mc, 1)

        # Center label
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

        # Needle
        val_frac = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        needle_angle = start_angle - val_frac * sweep
        self._draw_needle(p, cx, cy, radius, needle_angle)

    # ── Combo gauge (fuel + coolant sharing one dial) ────────────────

    def _draw_combo_gauge(self, p, cx, cy, radius,
                          val_left, min_l, max_l, label_l, lo_l, hi_l,
                          val_right, min_r, max_r, label_r, lo_r, hi_r,
                          redline_right=None):
        self._draw_bezel(p, cx, cy, radius)
        self._draw_face(p, cx, cy, radius)

        # Left arc: fuel (225 -> 180, ~45 deg sweep on the left side)
        left_start = 225
        left_sweep = 90
        lfrac = max(0.0, min(1.0, (val_left - min_l) / (max_l - min_l)))

        for pos, lbl in [(0.0, lo_l), (0.5, "1/2"), (1.0, hi_l)]:
            angle = math.radians(left_start - pos * left_sweep)
            self._tick_line(p, cx, cy, radius - 20, radius - 6, angle, theme.TICK_WHITE, 2)
            self._tick_label(p, cx, cy, radius - 32, angle, lbl,
                             max(7, radius // 20), theme.TICK_WHITE)

        la = left_start - lfrac * left_sweep
        self._draw_needle(p, cx, cy, radius, la)

        # Right arc: coolant (315 -> 360, ~90 deg sweep on the right side)
        right_start = 315
        right_sweep = 90
        rfrac = max(0.0, min(1.0, (val_right - min_r) / (max_r - min_r)))

        ticks_r = [40, 60, 80, 100, 120, 130]
        for tv in ticks_r:
            pos = (tv - min_r) / (max_r - min_r)
            angle = math.radians(right_start + pos * right_sweep)
            in_red = redline_right is not None and tv >= redline_right
            c = theme.NEEDLE_RED if in_red else theme.TICK_WHITE
            self._tick_line(p, cx, cy, radius - 20, radius - 6, angle, c, 2)
            self._tick_label(p, cx, cy, radius - 32, angle, str(int(tv)),
                             max(7, radius // 20), c)

        # Redline arc for coolant
        if redline_right is not None:
            rs = (redline_right - min_r) / (max_r - min_r)
            sa = right_start + rs * right_sweep
            ea = right_start + right_sweep
            self._draw_arc_segment(p, cx, cy, radius - 8, sa, ea - sa, theme.NEEDLE_RED)

        # Labels
        lf = theme.gauge_font(max(7, radius // 20))
        p.setFont(lf)
        p.setPen(theme.TICK_DIM)
        fm = QFontMetrics(lf)
        p.drawText(QPointF(cx - radius * 0.5, cy + radius * 0.15), "FUEL")
        p.drawText(QPointF(cx + radius * 0.15, cy + radius * 0.15), "\u00b0C")

    # ── Analog clock ─────────────────────────────────────────────────

    def _draw_clock(self, p, cx, cy, radius):
        self._draw_bezel(p, cx, cy, radius)
        self._draw_face(p, cx, cy, radius)

        # Hour markers
        for h in range(12):
            angle = math.radians(90 - h * 30)
            r_out = radius - 6
            r_in = radius - 16 if h % 3 == 0 else radius - 12
            self._tick_line(p, cx, cy, r_in, r_out, angle, theme.TICK_WHITE,
                            2 if h % 3 == 0 else 1)
            if h % 3 == 0:
                label = str(h if h > 0 else 12)
                self._tick_label(p, cx, cy, radius - 28, angle, label,
                                 max(7, radius // 20), theme.TICK_WHITE)

        now = time.localtime()
        hour_f = (now.tm_hour % 12) + now.tm_min / 60.0
        min_f = now.tm_min + now.tm_sec / 60.0

        # Hour hand
        ha = 90 - hour_f * 30
        self._draw_clock_hand(p, cx, cy, radius * 0.50, ha, 3, theme.TICK_WHITE)

        # Minute hand
        ma = 90 - min_f * 6
        self._draw_clock_hand(p, cx, cy, radius * 0.72, ma, 2, theme.TICK_WHITE)

        # Center dot
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(theme.TICK_WHITE))
        p.drawEllipse(QPointF(cx, cy), 4, 4)

    def _draw_clock_hand(self, p, cx, cy, length, angle_deg, width, color):
        angle = math.radians(angle_deg)
        nx = cx + length * math.cos(angle)
        ny = cy - length * math.sin(angle)
        p.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap))
        p.drawLine(QPointF(cx, cy), QPointF(nx, ny))

    # ── Bezel + face ─────────────────────────────────────────────────

    def _draw_bezel(self, p, cx, cy, radius):
        grad = QRadialGradient(cx, cy, radius + 6)
        grad.setColorAt(0.90, theme.BEZEL_DARK)
        grad.setColorAt(0.95, theme.BEZEL_HIGHLIGHT)
        grad.setColorAt(1.00, theme.BEZEL_DARK)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(grad))
        p.drawEllipse(QPointF(cx, cy), radius + 6, radius + 6)

    def _draw_face(self, p, cx, cy, radius):
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(theme.GAUGE_FACE))
        p.drawEllipse(QPointF(cx, cy), radius, radius)

    # ── Needle (tapered polygon + shadow) ─────────────────────────────

    def _draw_needle(self, p, cx, cy, radius, angle_deg):
        angle = math.radians(angle_deg)
        perp = angle + math.pi / 2
        tip_len = radius - 24
        tail_len = radius * 0.15
        half_base = 2.5
        half_tip = 0.5

        tip = QPointF(cx + tip_len * math.cos(angle),
                       cy - tip_len * math.sin(angle))
        tail = QPointF(cx - tail_len * math.cos(angle),
                        cy + tail_len * math.sin(angle))
        base_l = QPointF(cx + half_base * math.cos(perp),
                          cy - half_base * math.sin(perp))
        base_r = QPointF(cx - half_base * math.cos(perp),
                          cy + half_base * math.sin(perp))
        tip_l = QPointF(tip.x() + half_tip * math.cos(perp),
                         tip.y() - half_tip * math.sin(perp))
        tip_r = QPointF(tip.x() - half_tip * math.cos(perp),
                         tip.y() + half_tip * math.sin(perp))

        needle_poly = QPolygonF([tail, base_l, tip_l, tip_r, base_r])

        # Shadow
        shadow_offset = 2
        shadow_poly = QPolygonF()
        for pt in needle_poly:
            shadow_poly.append(QPointF(pt.x() + shadow_offset, pt.y() + shadow_offset))
        p.setPen(Qt.NoPen)
        shadow_c = QColor(0, 0, 0, 100)
        p.setBrush(QBrush(shadow_c))
        p.drawPolygon(shadow_poly)

        # Needle body
        p.setBrush(QBrush(theme.NEEDLE_AMBER))
        p.setPen(QPen(QColor(180, 110, 20), 0.5))
        p.drawPolygon(needle_poly)

        # Hub cap
        hub_grad = QRadialGradient(cx - 1, cy - 1, 8)
        hub_grad.setColorAt(0.0, QColor(120, 115, 105))
        hub_grad.setColorAt(0.6, QColor(70, 68, 62))
        hub_grad.setColorAt(1.0, QColor(40, 38, 34))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(hub_grad))
        p.drawEllipse(QPointF(cx, cy), 7, 7)

    # ── Tick helpers ──────────────────────────────────────────────────

    def _tick_line(self, p, cx, cy, r_in, r_out, angle, color, width):
        p.setPen(QPen(color, width))
        p.drawLine(
            QPointF(cx + r_in * math.cos(angle), cy - r_in * math.sin(angle)),
            QPointF(cx + r_out * math.cos(angle), cy - r_out * math.sin(angle)),
        )

    def _tick_label(self, p, cx, cy, r_text, angle, text, font_size, color):
        f = theme.gauge_font(font_size)
        p.setFont(f)
        p.setPen(color)
        fm = QFontMetrics(f)
        tx = cx + r_text * math.cos(angle) - fm.horizontalAdvance(text) / 2
        ty = cy - r_text * math.sin(angle) + fm.ascent() / 2
        p.drawText(QPointF(tx, ty), text)

    # ── Arc segments ─────────────────────────────────────────────────

    def _draw_redline_arc(self, p, cx, cy, radius, min_val, max_val,
                          rl_start, rl_end, start_angle, sweep):
        s_frac = (rl_start - min_val) / (max_val - min_val)
        e_frac = (rl_end - min_val) / (max_val - min_val)
        arc_start = start_angle - s_frac * sweep
        arc_end = start_angle - e_frac * sweep
        self._draw_arc_segment(p, cx, cy, radius - 8, arc_end, arc_start - arc_end,
                               theme.NEEDLE_RED)

    def _draw_arc_segment(self, p, cx, cy, radius, start_deg, span_deg, color):
        pen = QPen(color, 3)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
        p.drawArc(rect, int(start_deg * 16), int(span_deg * 16))

    # ── Warning lights strip ─────────────────────────────────────────

    def _draw_warning_strip(self, p, w, h, vals):
        strip_y = h - 28
        icons = [
            ("\u25C1", False),   # left turn
            ("\u25B7", False),   # right turn
            ("\u26A0", False),   # warning triangle
            ("ASR", False),
            ("ABS", False),
            ("SRS", False),
            ("ADS", vals["ads_mode"] == "SPORT"),
            ("\u2623", False),   # oil pressure (placeholder)
        ]
        total_w = len(icons) * 80
        x0 = (w - total_w) // 2
        icon_font = theme.gauge_font(9, bold=True)
        p.setFont(icon_font)

        for i, (label, active) in enumerate(icons):
            x = x0 + i * 80
            color = theme.AMBER if active else QColor(30, 28, 25)
            p.setPen(color)
            fm = QFontMetrics(icon_font)
            tx = x + (80 - fm.horizontalAdvance(label)) // 2
            p.drawText(tx, strip_y + 16, label)
