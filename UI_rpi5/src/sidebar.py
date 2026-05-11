"""
R129 Driver UI -- Sidebar
128px vertical icon strip on the left edge with 8 page slots.
Icons are 9x9 dot-matrix pixel art, matching the retro LCD aesthetic.
Selected icon is inverted (amber-filled slot, dark icon dots).

Bottom of the sidebar carries an always-visible audio footer:
  ▲ tap zone (volume up +5%)
  thin volume bar (8 segments)
  ▼ tap zone (volume down -5%)
  percentage readout
  clock (existing)
The audio footer stays visible even when the CarPlay (LIVI) window is
in foreground, because labwc rules confine LIVI to x = SIDEBAR_WIDTH.
"""

import time

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QColor, QFontMetrics

import theme

ICON_W = 9
ICON_H = 9
ICON_DOT = 4.2
ICON_SPACING = 7.0

# ── Audio footer layout (bottom of sidebar) ──────────────────────────
# Sized for a 1920x1080 portrait sidebar = 128 wide, 1080 tall.
# Each of these values is in raw pixels; only the vertical sum matters
# (it's subtracted from `h` before dividing the remainder among icon slots).
FOOTER_TOP_PAD = 8
TRI_H = 28              # up/down triangle vertical extent
TRI_GAP = 8             # gap between triangle and bar
BAR_H = 10              # height of the volume bar (single row of dots)
BAR_SEGMENTS = 8
BAR_DOT = 7.0           # dot diameter inside the bar
BAR_DOT_SPACING = 11.0  # centre-to-centre spacing of bar segments
LABEL_H = 14            # percentage readout
CLOCK_H = 14
FOOTER_INNER_GAP = 4
FOOTER_H = (FOOTER_TOP_PAD + TRI_H + TRI_GAP + BAR_H + TRI_GAP + TRI_H
            + FOOTER_INNER_GAP + LABEL_H + FOOTER_INNER_GAP + CLOCK_H + 6)

# Triangle bitmaps (5 rows × 9 cols, matching the 9-col icon convention).
_TRI_UP = [
    0b000010000,
    0b000111000,
    0b001111100,
    0b011111110,
    0b111111111,
]
_TRI_DOWN = [
    0b111111111,
    0b011111110,
    0b001111100,
    0b000111000,
    0b000010000,
]
_TRI_DOT = 3.4
_TRI_SPACING = 5.4

# 9x9 pixel art bitmaps (bit 8 = leftmost column)
_ICONS = {
    "home": [
        0b000010000,
        0b000111000,
        0b001111100,
        0b011111110,
        0b111111111,
        0b011000110,
        0b011000110,
        0b011010110,
        0b011111110,
    ],
    "classic": [  # speedometer arc + needle
        0b001111100,
        0b010000010,
        0b100000001,
        0b100001001,
        0b100010001,
        0b100100001,
        0b010000010,
        0b001111100,
        0b000000000,
    ],
    "modern": [  # 3-bar chart
        0b000000000,
        0b000010000,
        0b000010000,
        0b010010000,
        0b010010010,
        0b010010010,
        0b010010010,
        0b010010010,
        0b111111111,
    ],
    "diag": [  # warning triangle with !
        0b000010000,
        0b000010000,
        0b000101000,
        0b000101000,
        0b001000100,
        0b001010100,
        0b010000010,
        0b010010010,
        0b111111111,
    ],
    "settings": [  # gear
        0b010010010,
        0b001111100,
        0b011000110,
        0b110000011,
        0b011000110,
        0b110000011,
        0b011000110,
        0b001111100,
        0b010010010,
    ],
    "carplay": [  # phone/projection
        0b001111100,
        0b010000010,
        0b010010010,
        0b010111010,
        0b010010010,
        0b010000010,
        0b010000010,
        0b010000010,
        0b001111100,
    ],
    "map": [  # compass crosshair
        0b000010000,
        0b000010000,
        0b001111100,
        0b010010010,
        0b111010111,
        0b010010010,
        0b001111100,
        0b000010000,
        0b000010000,
    ],
    "exit": [  # power symbol (circle + top bar)
        0b000010000,
        0b000010000,
        0b010010010,
        0b010000010,
        0b100000001,
        0b100000001,
        0b010000010,
        0b010000010,
        0b001111100,
    ],
    "spare": [  # diamond (fallback)
        0b000010000,
        0b000101000,
        0b001000100,
        0b010000010,
        0b100000001,
        0b010000010,
        0b001000100,
        0b000101000,
        0b000010000,
    ],
}

PAGE_NAMES = [
    "home", "classic", "modern", "diag",
    "settings", "carplay", "map", "exit",
]


class Sidebar(QWidget):
    page_activated = pyqtSignal(int)

    def __init__(self, page_count: int = 8, audio=None, parent=None):
        super().__init__(parent)
        self._page_count = page_count
        self._selected = 0
        self._bright = True
        self._audio = audio
        self.setFixedWidth(theme.SIDEBAR_WIDTH)

        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self.update)
        self._clock_timer.start(10_000)

        if self._audio is not None:
            self._audio.volume_changed.connect(lambda _v: self.update())

    def set_selected(self, index: int):
        if self._selected != index:
            self._selected = index
            self.update()

    def set_bright(self, bright: bool):
        if self._bright != bright:
            self._bright = bright
            self.update()

    @property
    def selected(self) -> int:
        return self._selected

    def move_selection(self, delta: int):
        self._selected = (self._selected + delta) % self._page_count
        self.update()

    def _icon_area_height(self) -> int:
        """Vertical extent reserved for the 8 icon slots — anything below
        is the audio footer (▲ / bar / ▼ / percentage / clock)."""
        return max(0, self.height() - FOOTER_H)

    def mousePressEvent(self, event):
        y = int(event.y())
        icon_area = self._icon_area_height()

        # Audio footer hot zones — only when the controller is attached.
        if self._audio is not None and y >= icon_area:
            ftr_y = y - icon_area
            # ▲ zone: from top of footer through bottom of up-triangle
            tri_up_bottom = FOOTER_TOP_PAD + TRI_H
            # ▼ zone: starts after bar, runs through bottom of down-triangle
            tri_down_top = FOOTER_TOP_PAD + TRI_H + TRI_GAP + BAR_H + TRI_GAP
            tri_down_bottom = tri_down_top + TRI_H
            if ftr_y < tri_up_bottom:
                self._audio.nudge_up()
                return
            if tri_down_top <= ftr_y < tri_down_bottom:
                self._audio.nudge_down()
                return
            # Taps in the bar / readout / clock zone are intentionally ignored
            # (no drag interaction by design — see design doc).
            return

        # Above the footer: existing slot-selection behaviour.
        slot_h = max(1, icon_area // self._page_count)
        idx = y // slot_h
        idx = max(0, min(self._page_count - 1, idx))
        self._selected = idx
        self.update()
        self.page_activated.emit(idx)

    # ── Paint ────────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()

        p.fillRect(self.rect(), theme.SIDEBAR_BG)

        p.setPen(theme.SIDEBAR_SEPARATOR)
        p.drawLine(w - 1, 0, w - 1, h)

        icon_area = self._icon_area_height()
        slot_h = max(1, icon_area // self._page_count)

        for i in range(self._page_count):
            y = i * slot_h
            is_sel = (i == self._selected)

            if is_sel:
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(theme.AMBER))
                pad = 6
                p.drawRoundedRect(
                    QRectF(pad, y + pad, w - 2 * pad, slot_h - 2 * pad), 8, 8)

            name = PAGE_NAMES[i] if i < len(PAGE_NAMES) else "spare"
            bitmap = _ICONS.get(name, _ICONS["spare"])

            icon_total_w = ICON_W * ICON_SPACING
            icon_total_h = ICON_H * ICON_SPACING
            ix = (w - icon_total_w) / 2
            iy = y + (slot_h - icon_total_h) / 2

            if is_sel:
                on_color = QColor(theme.SIDEBAR_BG)
                on_color.setAlpha(240)
                off_color = QColor(theme.AMBER)
                off_color.setAlpha(60)
            else:
                base_alpha = 220 if self._bright else 120
                on_color = QColor(theme.AMBER)
                on_color.setAlpha(base_alpha)
                off_color = theme.DOT_OFF

            self._draw_pixel_icon(p, ix, iy, bitmap, on_color, off_color)

        # ── Audio footer (always painted when AudioController is attached) ──
        # On dev hosts without wpctl, the footer still renders so layout is
        # visible; the internal volume state is the source of truth.
        if self._audio is not None:
            self._paint_audio_footer(p, w, icon_area)

        # ── Clock at very bottom (always shown) ────────────────────────
        clock_alpha = 200 if self._bright else 100
        clock_color = QColor(theme.TICK_DIM)
        clock_color.setAlpha(clock_alpha)
        p.setPen(clock_color)
        cf = theme.gauge_font(10)
        p.setFont(cf)
        ts = time.strftime("%H:%M")
        fm = QFontMetrics(cf)
        p.drawText((w - fm.horizontalAdvance(ts)) // 2, h - 8, ts)

        p.end()

    def _draw_pixel_icon(self, p, x, y, bitmap, on_color, off_color):
        p.setPen(Qt.NoPen)
        for row in range(ICON_H):
            bits = bitmap[row] if row < len(bitmap) else 0
            for col in range(ICON_W):
                is_on = (bits >> (ICON_W - 1 - col)) & 1
                color = on_color if is_on else off_color
                p.setBrush(color)
                dx = x + col * ICON_SPACING
                dy = y + row * ICON_SPACING
                p.drawEllipse(QRectF(dx, dy, ICON_DOT, ICON_DOT))

    def _paint_audio_footer(self, p: QPainter, w: int, icon_area: int):
        """Render the ▲ / bar / ▼ / % readout below the icon slots.
        Clock is drawn separately by paintEvent (existing behaviour)."""
        vol = float(self._audio.volume)
        vol = max(0.0, min(1.0, vol))

        on_alpha = 220 if self._bright else 120
        dim_alpha = 90 if self._bright else 50
        on_color = QColor(theme.AMBER); on_color.setAlpha(on_alpha)
        dim_color = QColor(theme.AMBER); dim_color.setAlpha(dim_alpha)
        off_color = QColor(theme.DOT_OFF)

        # 1. Up triangle ───────────────────────────────────────────────
        tri_w = 9 * _TRI_SPACING
        tri_x = (w - tri_w) / 2.0
        tri_up_y = icon_area + FOOTER_TOP_PAD
        self._draw_triangle(p, tri_x, tri_up_y, _TRI_UP, on_color, off_color)

        # 2. Volume bar ────────────────────────────────────────────────
        bar_w = BAR_SEGMENTS * BAR_DOT_SPACING - (BAR_DOT_SPACING - BAR_DOT)
        bar_x = (w - bar_w) / 2.0
        bar_y = tri_up_y + TRI_H + TRI_GAP
        filled = int(round(vol * BAR_SEGMENTS))
        p.setPen(Qt.NoPen)
        for seg in range(BAR_SEGMENTS):
            p.setBrush(on_color if seg < filled else off_color)
            cx = bar_x + seg * BAR_DOT_SPACING
            p.drawEllipse(QRectF(cx, bar_y, BAR_DOT, BAR_DOT))

        # 3. Down triangle ─────────────────────────────────────────────
        tri_down_y = bar_y + BAR_H + TRI_GAP
        self._draw_triangle(p, tri_x, tri_down_y, _TRI_DOWN, on_color, off_color)

        # 4. Percentage readout ────────────────────────────────────────
        label_y = tri_down_y + TRI_H + FOOTER_INNER_GAP + LABEL_H
        p.setPen(dim_color)
        lf = theme.gauge_font(10)
        p.setFont(lf)
        pct = f"{int(round(vol * 100)):d} %"
        fm = QFontMetrics(lf)
        p.drawText((w - fm.horizontalAdvance(pct)) // 2, label_y, pct)

    def _draw_triangle(self, p: QPainter, x: float, y: float,
                       bitmap, on_color: QColor, off_color: QColor):
        """Render a 5-row dot-matrix triangle bitmap at (x, y)."""
        p.setPen(Qt.NoPen)
        for row, bits in enumerate(bitmap):
            for col in range(9):
                is_on = (bits >> (9 - 1 - col)) & 1
                if is_on:
                    p.setBrush(on_color)
                else:
                    p.setBrush(off_color)
                dx = x + col * _TRI_SPACING
                dy = y + row * _TRI_SPACING
                p.drawEllipse(QRectF(dx, dy, _TRI_DOT, _TRI_DOT))
