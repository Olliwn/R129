"""
R129 Driver UI -- Exit View
Last sidebar slot. Quits the UI so the underlying Linux desktop is exposed.
Activation is explicit: rotary PRESS, or a touch hold of ``theme.TOUCH_HOLD_MS``
inside the view (mirrors the CarPlay-stop hold pattern). A single quick tap
does nothing -- this is a destructive action and we don't want an accidental
finger brush on a pothole to drop the user out of the UI.

Restarting the UI is handled outside this app (desktop icon / systemd).
"""

import time

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush

import theme
from dot_matrix import draw_dot_text, dot_line_height
from input_actions import InputAction


class ExitView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hold_state: str | None = None  # None | "short" | "long"
        self._hold_started_ms: int = 0
        self._hold_timer = QTimer(self)
        self._hold_timer.setSingleShot(True)
        self._hold_timer.setInterval(theme.TOUCH_HOLD_MS)
        self._hold_timer.timeout.connect(self._on_hold_threshold)

        self._tick_timer = QTimer(self)
        self._tick_timer.setInterval(33)
        self._tick_timer.timeout.connect(self.update)

    def handle_input(self, action: InputAction):
        if action == InputAction.PRESS:
            self._quit()
            return True
        if action == InputAction.LEFT:
            return "back"
        return False

    def on_hidden(self):
        self._cancel_hold()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        self._hold_state = "short"
        self._hold_started_ms = int(time.monotonic() * 1000)
        self._hold_timer.start()
        self._tick_timer.start()
        self.update()

    def mouseReleaseEvent(self, event):
        if self._hold_state is None:
            return
        state = self._hold_state
        self._cancel_hold()
        if state == "long":
            self._quit()

    def _on_hold_threshold(self):
        if self._hold_state == "short":
            self._hold_state = "long"
            self.update()

    def _cancel_hold(self):
        self._hold_state = None
        self._hold_started_ms = 0
        self._hold_timer.stop()
        self._tick_timer.stop()
        self.update()

    def _quit(self):
        app = QApplication.instance()
        if app is not None:
            app.quit()

    def _hold_progress(self) -> float:
        """0.0..1.0 fraction of the touch-hold threshold elapsed."""
        if self._hold_state is None or self._hold_started_ms == 0:
            return 0.0
        now_ms = int(time.monotonic() * 1000)
        elapsed = now_ms - self._hold_started_ms
        return max(0.0, min(1.0, elapsed / float(theme.TOUCH_HOLD_MS)))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillRect(self.rect(), theme.BG)

        w, h = self.width(), self.height()
        lh = dot_line_height()
        cx = w * 0.08
        cy = h * 0.22

        draw_dot_text(p, cx, cy, "EXIT TO DESKTOP")
        cy += lh * 2.0
        if self._hold_state == "long":
            draw_dot_text(p, cx, cy, "RELEASE TO QUIT",
                          on_color=theme.NEEDLE_RED)
        elif self._hold_state == "short":
            draw_dot_text(p, cx, cy, "HOLD TO CONFIRM...",
                          on_color=theme.AMBER)
        else:
            draw_dot_text(p, cx, cy, "HOLD TO QUIT",
                          on_color=theme.AMBER_DIM)
        cy += lh * 1.3
        draw_dot_text(p, cx, cy, "RESTART VIA DESKTOP ICON",
                      on_color=theme.AMBER_DIM)

        # Hold progress bar — visible feedback that the finger can't cover.
        # Placed well below the text so the user sees it filling even when
        # tapping the centre of the screen.
        if self._hold_state is not None:
            cy += lh * 2.5
            bar_x = cx
            bar_w = w * 0.55
            bar_h = 18
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(theme.AMBER_DARK))
            p.drawRoundedRect(QRectF(bar_x, cy, bar_w, bar_h), 4, 4)
            frac = self._hold_progress()
            fill_w = bar_w * frac
            fill_color = (QColor(theme.NEEDLE_RED) if self._hold_state == "long"
                          else QColor(theme.AMBER))
            p.setBrush(QBrush(fill_color))
            p.drawRoundedRect(QRectF(bar_x, cy, fill_w, bar_h), 4, 4)

        p.end()
