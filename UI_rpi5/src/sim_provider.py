"""
R129 Driver UI -- Simulated Data Provider
Generates slowly oscillating demo telemetry and writes it into a VehicleState.
Drop-in replacement for the future BLE provider during development.
"""

import math
import time

from PyQt5.QtCore import QObject, QTimer

from vehicle_state import VehicleState


class SimulatedProvider(QObject):
    """Drives a ``VehicleState`` with sine-wave demo values at ~30 Hz."""

    def __init__(self, state: VehicleState, parent=None):
        super().__init__(parent)
        self._state = state
        self._t0 = time.monotonic()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(33)  # ~30 fps, matches gauge repaint rate

    def _tick(self):
        t = time.monotonic() - self._t0
        self._state.rpm = 800 + 400 * math.sin(t * 0.3) + 200 * math.sin(t * 0.7)
        self._state.speed = 60 + 30 * math.sin(t * 0.2) + 10 * math.sin(t * 0.5)
        self._state.coolant = 85 + 5 * math.sin(t * 0.15)
        self._state.oil_temp = 90 + 8 * math.sin(t * 0.1)
        self._state.fuel = 65 + 10 * math.sin(t * 0.05)
        self._state.voltage = 13.8 + 0.3 * math.sin(t * 0.4)
        self._state.ads_mode = "SPORT" if int(t) % 10 < 5 else "COMFORT"
