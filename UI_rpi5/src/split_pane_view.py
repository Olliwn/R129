"""
R129 Driver UI -- Split-Pane View
Reusable base class for Tesla-style left-list / right-detail layout.
Internal navigation states: "list", "detail", "param".

  list:   UP/DOWN scroll categories, PRESS/RIGHT enters detail, LEFT -> "back" to sidebar
  detail: UP/DOWN scroll detail options, PRESS on editable item -> param, LEFT -> list
  param:  CW/CCW or LEFT/RIGHT adjust value, PRESS accepts, LEFT cancels -> detail

All text rendered in dot-matrix style for consistent retro aesthetic.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QFontMetrics, QColor

import theme
from input_actions import InputAction
from dot_matrix import draw_dot_text, dot_line_height, dot_text_width

LEFT_RATIO = 0.24
ITEM_HEIGHT = 68
TOP_MARGIN = 21
LEFT_TEXT_X = 30


class SplitPaneView(QWidget):

    def __init__(self):
        super().__init__()
        self._items: list[str] = []
        self._selected = 0
        self._scroll_offset = 0
        self._focus = "list"
        self._detail_selected = 0
        self._detail_count = 0

        self._param_editing = False
        self._param_key = ""
        self._param_value = 0
        self._param_old = 0
        self._param_min = 0
        self._param_max = 100

    def handle_input(self, action: InputAction):
        if self._focus == "list":
            return self._handle_list(action)
        elif self._focus == "param":
            return self._handle_param(action)
        else:
            return self._handle_detail(action)

    def _handle_list(self, action: InputAction):
        if action in (InputAction.UP, InputAction.CCW):
            self._move(-1)
        elif action in (InputAction.DOWN, InputAction.CW):
            self._move(1)
        elif action in (InputAction.PRESS, InputAction.RIGHT):
            self._focus = "detail"
            self._detail_selected = 0
            self.update()
        elif action == InputAction.LEFT:
            return "back"

    def _handle_detail(self, action: InputAction):
        if action in (InputAction.UP, InputAction.CCW):
            self._detail_selected = max(0, self._detail_selected - 1)
            self.update()
        elif action in (InputAction.DOWN, InputAction.CW):
            if self._detail_count > 0:
                self._detail_selected = min(self._detail_count - 1,
                                            self._detail_selected + 1)
            self.update()
        elif action == InputAction.LEFT:
            self._focus = "list"
            self.update()
        elif action in (InputAction.PRESS, InputAction.RIGHT):
            self._on_detail_press(self._detail_selected)

    def _handle_param(self, action: InputAction):
        if action in (InputAction.CW, InputAction.RIGHT):
            self._param_value = min(self._param_max, self._param_value + 1)
            self.update()
        elif action in (InputAction.CCW, InputAction.LEFT):
            self._param_value = max(self._param_min, self._param_value - 1)
            self.update()
        elif action == InputAction.PRESS:
            self._focus = "detail"
            self._on_param_done(self._param_key, self._param_value, cancelled=False)
            self.update()

    def _on_detail_press(self, detail_index: int):
        """Override in subclass to handle PRESS on a detail item."""
        pass

    def _on_param_done(self, key: str, value: int, cancelled: bool):
        """Override in subclass when param editing completes."""
        pass

    def start_param_edit(self, key: str, value: int, min_v: int = 0, max_v: int = 100):
        self._focus = "param"
        self._param_key = key
        self._param_value = value
        self._param_old = value
        self._param_min = min_v
        self._param_max = max_v
        self.update()

    def _move(self, delta: int):
        if not self._items:
            return
        self._selected = max(0, min(len(self._items) - 1, self._selected + delta))
        self._ensure_visible()
        self.update()

    def _ensure_visible(self):
        h = self.height()
        visible_count = max(1, (h - TOP_MARGIN) // ITEM_HEIGHT)
        if self._selected < self._scroll_offset:
            self._scroll_offset = self._selected
        elif self._selected >= self._scroll_offset + visible_count:
            self._scroll_offset = self._selected - visible_count + 1

    # ── Paint ────────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), theme.BG)

        left_w = int(w * LEFT_RATIO)
        self._draw_left(p, left_w, h)

        in_detail = self._focus in ("detail", "param")
        div_color = theme.AMBER_DIM if in_detail else theme.SIDEBAR_SEPARATOR
        p.setPen(QPen(div_color, 2 if in_detail else 1))
        p.drawLine(left_w, 0, left_w, h)

        detail_rect = QRectF(left_w + 16, TOP_MARGIN, w - left_w - 28, h - TOP_MARGIN - 8)
        self._draw_detail(p, detail_rect, self._selected)

        p.end()

    def _draw_left(self, p, left_w, h):
        list_active = (self._focus == "list")
        lh = dot_line_height()

        p.save()
        p.setClipRect(QRectF(0, 0, left_w - 4, h))

        usable_h = h - TOP_MARGIN
        visible_count = max(1, usable_h // ITEM_HEIGHT)
        for vi in range(visible_count):
            idx = self._scroll_offset + vi
            if idx >= len(self._items):
                break
            y = TOP_MARGIN + vi * ITEM_HEIGHT
            is_sel = (idx == self._selected)

            if is_sel:
                bg = QColor(40, 30, 8) if list_active else QColor(25, 22, 12)
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(bg))
                p.drawRect(QRectF(0, y, left_w, ITEM_HEIGHT))

                bar_color = theme.AMBER if list_active else theme.AMBER_DARK
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(bar_color))
                p.drawRect(QRectF(0, y, 4, ITEM_HEIGHT))

            if is_sel:
                on_color = theme.AMBER if list_active else theme.AMBER_DIM
            else:
                on_color = theme.AMBER_DIM if list_active else theme.AMBER_DARK

            text_y = y + (ITEM_HEIGHT - lh) / 2 + 2
            draw_dot_text(p, LEFT_TEXT_X, text_y, self._items[idx], on_color=on_color)

        p.restore()

    def _draw_detail(self, p, rect: QRectF, index: int):
        """Override in subclass to render detail for the selected item."""
        lh = dot_line_height()
        draw_dot_text(p, rect.x(), rect.y(), "NO DETAIL", on_color=theme.TICK_DIM)
