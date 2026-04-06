"""
R129 Driver UI -- Application Entry Point
Launches a fullscreen PyQt5 application on the Waveshare 5.5" AMOLED.
On desktop (macOS/Linux), runs windowed for development.
"""

import sys
import os
import pathlib


def _load_dotenv():
    """Load KEY=VALUE pairs from ../. env into os.environ."""
    env_path = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), val)


_load_dotenv()

from input_manager import _is_rpi

if _is_rpi():
    os.environ.setdefault("QT_QPA_PLATFORM", "wayland")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("R129 Driver UI")

    window = MainWindow()

    if _is_rpi():
        app.setOverrideCursor(Qt.BlankCursor)
        window.showFullScreen()
    else:
        window.resize(1920, 1080)
        window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
