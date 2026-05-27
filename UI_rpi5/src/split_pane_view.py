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

        # Touch / hit-test infrastructure.
        # `_left_item_rects` is populated by `_draw_left` each paint. Each
        # entry is (item_index, QRectF). `_detail_item_rects` is populated
        # by subclass `_draw_detail` overrides via `_register_detail_item`
        # — list of (item_index, QRectF). `_param_bar_rect` is set by the
        # subclass via `_register_param_bar` during param mode, used for
        # tap-to-set + drag-to-scrub.
        self._left_item_rects: list[tuple[int, QRectF]] = []
        self._detail_item_rects: list[tuple[int, QRectF]] = []
        self._param_bar_rect: QRectF | None = None
        self._scrubbing_param = False

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

    # ── Touch input ──────────────────────────────────────────────────
    # Mouse events synthesize the same internal state changes the
    # rotary/keyboard path uses. Both input sources coexist; tapping
    # never breaks the rotary flow and vice versa.

    def _register_detail_item(self, index: int, rect: QRectF):
        """Subclasses call this during ``_draw_detail`` so taps can be
        mapped back to the originating item. Resets each paint."""
        self._detail_item_rects.append((index, rect))

    def _register_param_bar(self, rect: QRectF):
        """Subclass call from inside ``_draw_param_bar`` so tap+drag on
        the slider can update ``_param_value`` directly. Cleared on
        param exit."""
        self._param_bar_rect = rect

    def _hit_left(self, x: float, y: float) -> int:
        for idx, rect in self._left_item_rects:
            if rect.contains(x, y):
                return idx
        return -1

    def _hit_detail(self, x: float, y: float) -> int:
        for idx, rect in self._detail_item_rects:
            if rect.contains(x, y):
                return idx
        return -1

    def _set_param_from_x(self, x: float):
        if self._param_bar_rect is None:
            return
        r = self._param_bar_rect
        frac = (x - r.x()) / r.width() if r.width() > 0 else 0.0
        frac = max(0.0, min(1.0, frac))
        value = round(self._param_min
                      + frac * (self._param_max - self._param_min))
        if value != self._param_value:
            self._param_value = int(value)
            self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        x, y = event.x(), event.y()

        # Scrubbing the param bar takes priority — keeps the slider feel
        # tight when the user lands their finger directly on the bar.
        if (self._focus == "param" and self._param_bar_rect is not None
                and self._param_bar_rect.contains(x, y)):
            self._scrubbing_param = True
            self._set_param_from_x(x)
            return

        # Left pane: category list. Tap to select + jump into detail.
        # Tap on the already-selected category retreats to list focus
        # (matches the rotary LEFT shortcut from detail back to list).
        left_idx = self._hit_left(x, y)
        if left_idx >= 0:
            if self._focus == "param":
                # Commit current value before navigating away.
                self._focus = "detail"
                self._on_param_done(self._param_key,
                                    self._param_value, cancelled=False)
                self._param_bar_rect = None
            if left_idx == self._selected and self._focus == "detail":
                self._focus = "list"
            else:
                self._selected = left_idx
                self._focus = "detail"
                self._detail_selected = 0
            self.update()
            return

        # Right pane: detail items. Tap to activate (toggle or enter
        # param edit). Works from any focus — taps from "list" focus
        # implicitly enter "detail" focus first, so the user doesn't
        # have to tap the category and then the option.
        det_idx = self._hit_detail(x, y)
        if det_idx >= 0:
            if self._focus == "param":
                self._focus = "detail"
                self._on_param_done(self._param_key,
                                    self._param_value, cancelled=False)
                self._param_bar_rect = None
                if det_idx == self._detail_selected:
                    # Tapped the currently-edited slider item — just
                    # commit, don't re-enter edit mode.
                    self.update()
                    return
            elif self._focus == "list":
                self._focus = "detail"
            self._detail_selected = det_idx
            self._on_detail_press(det_idx)
            self.update()
            return

        # Tap on empty area inside the detail pane: cancel/commit param.
        if self._focus == "param":
            self._focus = "detail"
            self._on_param_done(self._param_key,
                                self._param_value, cancelled=False)
            self._param_bar_rect = None
            self.update()

    def mouseMoveEvent(self, event):
        if not self._scrubbing_param:
            return
        self._set_param_from_x(event.x())

    def mouseReleaseEvent(self, event):
        if not self._scrubbing_param:
            return
        self._scrubbing_param = False
        # Commit the scrubbed value and exit param mode in one motion —
        # the iOS-style "release to apply" gesture that feels natural
        # next to the rotary's modal CW/CCW/PRESS flow.
        self._focus = "detail"
        self._on_param_done(self._param_key,
                            self._param_value, cancelled=False)
        self._param_bar_rect = None
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

        # Reset hit-test rect lists each frame — they're repopulated by
        # `_draw_left` and the subclass `_draw_detail` overrides.
        self._left_item_rects = []
        self._detail_item_rects = []
        if self._focus != "param":
            self._param_bar_rect = None

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

            # Register the full-row rect as the touch target for this
            # category. Includes the left-edge accent bar zone so taps
            # anywhere on the row count.
            self._left_item_rects.append(
                (idx, QRectF(0, y, left_w, ITEM_HEIGHT)))

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
