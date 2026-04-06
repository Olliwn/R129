"""
R129 Driver UI -- Vehicle State Model
Central data store for all vehicle telemetry. Data providers (simulated, BLE)
write values here; UI views connect to the change signals.
"""

from PyQt5.QtCore import QObject, pyqtSignal


class VehicleState(QObject):
    """Observable vehicle telemetry state.

    Each field has a corresponding ``<field>_changed`` signal emitted only
    when the value actually changes.  Views connect to these signals to
    repaint only when data moves.
    """

    rpm_changed = pyqtSignal(float)
    speed_changed = pyqtSignal(float)
    coolant_changed = pyqtSignal(float)
    oil_temp_changed = pyqtSignal(float)
    fuel_changed = pyqtSignal(float)
    voltage_changed = pyqtSignal(float)
    ads_mode_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rpm: float = 0.0
        self._speed: float = 0.0
        self._coolant: float = 0.0
        self._oil_temp: float = 0.0
        self._fuel: float = 0.0
        self._voltage: float = 0.0
        self._ads_mode: str = "COMFORT"

    # ── Properties with change-gated setters ──────────────────────────

    @property
    def rpm(self) -> float:
        return self._rpm

    @rpm.setter
    def rpm(self, v: float):
        if self._rpm != v:
            self._rpm = v
            self.rpm_changed.emit(v)

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, v: float):
        if self._speed != v:
            self._speed = v
            self.speed_changed.emit(v)

    @property
    def coolant(self) -> float:
        return self._coolant

    @coolant.setter
    def coolant(self, v: float):
        if self._coolant != v:
            self._coolant = v
            self.coolant_changed.emit(v)

    @property
    def oil_temp(self) -> float:
        return self._oil_temp

    @oil_temp.setter
    def oil_temp(self, v: float):
        if self._oil_temp != v:
            self._oil_temp = v
            self.oil_temp_changed.emit(v)

    @property
    def fuel(self) -> float:
        return self._fuel

    @fuel.setter
    def fuel(self, v: float):
        if self._fuel != v:
            self._fuel = v
            self.fuel_changed.emit(v)

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, v: float):
        if self._voltage != v:
            self._voltage = v
            self.voltage_changed.emit(v)

    @property
    def ads_mode(self) -> str:
        return self._ads_mode

    @ads_mode.setter
    def ads_mode(self, v: str):
        if self._ads_mode != v:
            self._ads_mode = v
            self.ads_mode_changed.emit(v)

    def snapshot(self) -> dict:
        """Return all current values as a plain dict (useful for rendering)."""
        return {
            "rpm": self._rpm,
            "speed": self._speed,
            "coolant": self._coolant,
            "oil_temp": self._oil_temp,
            "fuel": self._fuel,
            "voltage": self._voltage,
            "ads_mode": self._ads_mode,
        }
