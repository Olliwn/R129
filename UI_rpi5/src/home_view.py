"""
R129 Driver UI -- Home View
Low-pixel dot-matrix 3D rendering of the R129 wireframe.
Lines are rasterized onto a grid matching the text dot pitch, then drawn
as circular dots -- same aesthetic as the rest of the retro LCD UI.

Retro FX (when theme.retro_fx is True):
  - Glow bleed: off-pixels adjacent to on-pixels get a faint ghost
  - Refresh flicker: periodic global brightness dip
"""

import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPainter, QColor

import theme
from input_actions import InputAction
from vehicle_state import VehicleState
from r129_wireframe import EDGES
from dot_matrix import (draw_dot_text, dot_line_height, dot_text_width,
                        DOT_SIZE, DOT_SPACING)

FOCAL = 6.0
CAMERA_DIST = 12.0
DEFAULT_PITCH = 30.0
DEFAULT_YAW = 30.0
PITCH_MIN = -10.0
PITCH_MAX = 80.0
AUTO_ROTATE_SPEED = 0.15
GRID_PAD = 3
_NEIGHBOURS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def _bresenham(c0, r0, c1, r1):
    """Integer Bresenham line rasterisation, yields (col, row) tuples."""
    dc = abs(c1 - c0)
    dr = abs(r1 - r0)
    sc = 1 if c0 < c1 else -1
    sr = 1 if r0 < r1 else -1
    err = dc - dr
    c, r = c0, r0
    while True:
        yield (c, r)
        if c == c1 and r == r1:
            break
        e2 = err << 1
        if e2 > -dr:
            err -= dr
            c += sc
        if e2 < dc:
            err += dc
            r += sr


class HomeView(QWidget):
    def __init__(self, state: VehicleState):
        super().__init__()
        self._state = state
        self._yaw = DEFAULT_YAW
        self._pitch = DEFAULT_PITCH
        self._auto_rotate = True
        self._drag_x = None
        self._drag_y = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(33)

        self._idle_timer = QTimer(self)
        self._idle_timer.setSingleShot(True)
        self._idle_timer.setInterval(3000)
        self._idle_timer.timeout.connect(self._resume_auto)

    def handle_input(self, action: InputAction) -> bool:
        return False

    def _tick(self):
        if self._auto_rotate:
            self._yaw += AUTO_ROTATE_SPEED
        self.update()

    def _resume_auto(self):
        self._auto_rotate = True

    # ── Touch / mouse rotation ────────────────────────────────────────

    def mousePressEvent(self, event):
        self._drag_x = event.x()
        self._drag_y = event.y()
        self._auto_rotate = False
        self._idle_timer.stop()

    def mouseMoveEvent(self, event):
        if self._drag_x is not None:
            dx = event.x() - self._drag_x
            dy = event.y() - self._drag_y
            self._yaw += dx * 0.4
            self._pitch = max(PITCH_MIN, min(PITCH_MAX, self._pitch + dy * 0.3))
            self._drag_x = event.x()
            self._drag_y = event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        self._drag_x = None
        self._drag_y = None
        self._idle_timer.start()

    # ── 3D → 2D projection ────────────────────────────────────────────

    def _project(self, x, y, z, cos_y, sin_y, cos_t, sin_t, cx, cy, scale):
        rx = x * cos_y + z * sin_y
        ry = y
        rz = -x * sin_y + z * cos_y
        ry2 = ry * cos_t - rz * sin_t
        rz2 = ry * sin_t + rz * cos_t
        d = CAMERA_DIST - rz2
        if d < 0.5:
            d = 0.5
        sx = cx + (FOCAL * rx / d) * scale
        sy = cy - (FOCAL * ry2 / d) * scale
        return sx, sy, d

    # ── Paint ─────────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), theme.BG)

        sp = DOT_SPACING * theme.DOT_SCALE
        ds = DOT_SIZE * theme.DOT_SCALE

        cx, cy = w / 2, h * 0.52
        scale = min(w, h) * 0.14

        yaw_r = math.radians(self._yaw)
        tilt_r = math.radians(self._pitch)
        cos_y, sin_y = math.cos(yaw_r), math.sin(yaw_r)
        cos_t, sin_t = math.cos(tilt_r), math.sin(tilt_r)

        # rasterise all 3D edges into the dot grid
        current = {}
        for (x0, y0, z0), (x1, y1, z1) in EDGES:
            sx0, sy0, d0 = self._project(x0, y0, z0, cos_y, sin_y,
                                          cos_t, sin_t, cx, cy, scale)
            sx1, sy1, d1 = self._project(x1, y1, z1, cos_y, sin_y,
                                          cos_t, sin_t, cx, cy, scale)
            gc0 = int(round(sx0 / sp))
            gr0 = int(round(sy0 / sp))
            gc1 = int(round(sx1 / sp))
            gr1 = int(round(sy1 / sp))
            avg_d = (d0 + d1) * 0.5
            intensity = max(0.35, min(1.0, 1.0 - (avg_d - 6.0) / 14.0))

            for gc, gr in _bresenham(gc0, gr0, gc1, gr1):
                prev = current.get((gc, gr), 0.0)
                if intensity > prev:
                    current[(gc, gr)] = intensity

        fx = theme.retro_fx

        # glow bleed: off-pixel neighbors of on-pixels get faint glow
        if fx:
            glow_alpha = theme.GLOW_BLEED_ALPHA
            glow_adds = {}
            for (c, r), intensity in current.items():
                g = intensity * glow_alpha
                for dc, dr in _NEIGHBOURS_4:
                    nc, nr = c + dc, r + dr
                    if (nc, nr) not in current:
                        if g > glow_adds.get((nc, nr), 0.0):
                            glow_adds[(nc, nr)] = g
            for key, val in glow_adds.items():
                current[key] = val

        # flicker
        flicker_mul = theme.FLICKER_DIM if (fx and theme.is_flicker_frame()) else 1.0

        if current:
            cols = [k[0] for k in current]
            rows = [k[1] for k in current]
            c_min = min(cols) - GRID_PAD
            c_max = max(cols) + GRID_PAD
            r_min = min(rows) - GRID_PAD
            r_max = max(rows) + GRID_PAD

            off_color = theme.DOT_OFF
            base_g = theme.VECTOR_GREEN
            p.setPen(Qt.NoPen)

            for r in range(r_min, r_max + 1):
                py = r * sp
                for c in range(c_min, c_max + 1):
                    px = c * sp
                    intensity = current.get((c, r))
                    if intensity is not None:
                        color = QColor(base_g)
                        color.setAlphaF(min(1.0, intensity * flicker_mul))
                    else:
                        color = off_color
                    p.setBrush(color)
                    p.drawEllipse(QRectF(px, py, ds, ds))

        self._draw_overlay(p, w, h)
        p.end()

    # ── Status overlay ────────────────────────────────────────────────

    def _draw_overlay(self, p, w, h):
        vals = self._state.snapshot()
        lh = dot_line_height()
        margin = 16

        green_dim = QColor(theme.VECTOR_GREEN)
        green_dim.setAlpha(160)

        row1 = f"{vals['voltage']:.1f}V  {vals['coolant']:.0f}C  OIL {vals['oil_temp']:.0f}C"
        rw1 = dot_text_width(row1)
        draw_dot_text(p, (w - rw1) / 2, margin, row1, on_color=green_dim)

        row2 = f"{vals['speed']:.0f}KMH  {vals['rpm']:.0f}RPM  ADS {vals['ads_mode']}"
        rw2 = dot_text_width(row2)
        draw_dot_text(p, (w - rw2) / 2, margin + lh, row2, on_color=green_dim)

        title = "R129 500SL AOK912"
        tw = dot_text_width(title)
        draw_dot_text(p, (w - tw) / 2, h - lh - 8, title, on_color=green_dim)
