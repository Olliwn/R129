"""
R129 Driver UI -- Application Entry Point
Launches a fullscreen PyQt5 application on the Waveshare 5.5" AMOLED.
"""

import sys
import os

os.environ.setdefault("QT_QPA_PLATFORM", "wayland")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("R129 Driver UI")
    app.setOverrideCursor(Qt.BlankCursor)

    window = MainWindow()
    window.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
