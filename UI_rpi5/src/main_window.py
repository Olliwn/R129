"""
R129 Driver UI -- Main Window
Fullscreen container with stacked views (gauges, future: settings, carplay).
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from gauge_view import GaugeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.gauge_view = GaugeView()
        self.stack.addWidget(self.gauge_view)

        self.stack.setCurrentWidget(self.gauge_view)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        super().keyPressEvent(event)
