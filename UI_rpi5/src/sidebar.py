"""
R129 Driver UI -- Sidebar
128px vertical icon strip on the left edge with 8 page slots.
Icons are 9x9 dot-matrix pixel art, matching the retro LCD aesthetic.
Selected icon is inverted (amber-filled slot, dark icon dots).
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

    def __init__(self, page_count: int = 8, parent=None):
        super().__init__(parent)
        self._page_count = page_count
        self._selected = 0
        self._bright = True
        self.setFixedWidth(theme.SIDEBAR_WIDTH)

        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self.update)
        self._clock_timer.start(10_000)

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

    def mousePressEvent(self, event):
        slot_h = self.height() // self._page_count
        idx = int(event.y()) // slot_h
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

        slot_h = h // self._page_count

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

        # clock at very bottom
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
