"""
R129 Driver UI -- Exit View
Last sidebar slot. Quits the UI so the underlying Linux desktop is exposed.
Activation is explicit (PRESS or tap inside the view), so reaching this page
by navigation alone does not exit.

Restarting the UI is handled outside this app (desktop icon / systemd).
"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter

import theme
from dot_matrix import draw_dot_text, dot_line_height
from input_actions import InputAction


class ExitView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_input(self, action: InputAction):
        if action == InputAction.PRESS:
            self._quit()
            return True
        if action == InputAction.LEFT:
            return "back"
        return False

    def mousePressEvent(self, event):
        self._quit()

    def _quit(self):
        app = QApplication.instance()
        if app is not None:
            app.quit()

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
        draw_dot_text(p, cx, cy, "TAP OR PRESS TO QUIT",
                      on_color=theme.AMBER_DIM)
        cy += lh * 1.3
        draw_dot_text(p, cx, cy, "RESTART VIA DESKTOP ICON",
                      on_color=theme.AMBER_DIM)

        p.end()
