"""
R129 Driver UI -- Placeholder View
Dot-matrix "coming soon" page for Media, Map, and Spare slots.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

import theme
from dot_matrix import draw_dot_text, dot_line_height
from input_actions import InputAction


class PlaceholderView(QWidget):
    def __init__(self, title: str = "RESERVED"):
        super().__init__()
        self._title = title

    def handle_input(self, action: InputAction):
        return False

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), theme.BG)

        lh = dot_line_height()
        cx = w * 0.08
        cy = h * 0.3

        draw_dot_text(p, cx, cy, self._title)
        draw_dot_text(p, cx, cy + lh * 1.5, "COMING SOON",
                      on_color=theme.AMBER_DIM)

        p.end()
