"""
R129 Driver UI -- Modem State Provider
Background thread that polls the nRF93M1 AT port for registration status,
signal strength (RSSI), operator name, and IP address.
Emits Qt signals so the UI can react without blocking.

Serial exceptions (e.g. port busy during bring-up) are caught silently;
the poller simply retries on the next cycle.
"""

import glob
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

BAUD = 115200
POLL_INTERVAL = 5


def _find_at_port():
    try:
        import serial
    except ImportError:
        return None
    for port in sorted(glob.glob("/dev/ttyACM*")):
        try:
            s = serial.Serial(port, BAUD, timeout=1)
            s.reset_input_buffer()
            s.write(b"AT\r\n")
            time.sleep(0.4)
            resp = s.read(s.in_waiting or 64).decode(errors="replace")
            s.close()
            if "OK" in resp:
                return port
        except Exception:
            continue
    return None


class ModemState(QObject):
    """Observable LTE modem state, polled in a background thread."""

    state_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lock = threading.Lock()
        self._enabled = True
        self._registered = False
        self._rssi_dbm = -999
        self._operator = ""
        self._ip = ""
        self._error = ""
        self._port = None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    # ── Public read API (thread-safe) ────────────────────────────────

    @property
    def enabled(self) -> bool:
        with self._lock:
            return self._enabled

    @property
    def registered(self) -> bool:
        with self._lock:
            return self._registered

    @property
    def rssi_dbm(self) -> int:
        with self._lock:
            return self._rssi_dbm

    @property
    def rssi_bars(self) -> int:
        """0-4 bar scale from dBm."""
        dbm = self.rssi_dbm
        if dbm <= -110 or dbm == -999:
            return 0
        if dbm <= -100:
            return 1
        if dbm <= -85:
            return 2
        if dbm <= -70:
            return 3
        return 4

    @property
    def operator(self) -> str:
        with self._lock:
            return self._operator

    @property
    def ip(self) -> str:
        with self._lock:
            return self._ip

    @property
    def error(self) -> str:
        with self._lock:
            return self._error

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "enabled": self._enabled,
                "registered": self._registered,
                "rssi_dbm": self._rssi_dbm,
                "rssi_bars": self.rssi_bars,
                "operator": self._operator,
                "ip": self._ip,
                "error": self._error,
            }

    # ── Enable/disable (triggers RNDIS teardown/bringup) ─────────────

    def set_enabled(self, on: bool):
        with self._lock:
            if self._enabled == on:
                return
            self._enabled = on
        if not on:
            self._teardown()
        self.state_changed.emit()

    # ── Background polling ───────────────────────────────────────────

    def _poll_loop(self):
        while not self._stop.wait(POLL_INTERVAL):
            with self._lock:
                if not self._enabled:
                    self._registered = False
                    self._rssi_dbm = -999
                    self._operator = ""
                    self._ip = ""
                    self._error = "DISABLED"
                    continue
            self._poll_once()
            try:
                self.state_changed.emit()
            except RuntimeError:
                break

    def _poll_once(self):
        try:
            import serial
        except ImportError:
            with self._lock:
                self._error = "NO PYSERIAL"
            return

        port = self._port or _find_at_port()
        if not port:
            with self._lock:
                self._registered = False
                self._rssi_dbm = -999
                self._error = "NO MODEM"
            return
        self._port = port

        try:
            ser = serial.Serial(port, BAUD, timeout=1)
        except Exception:
            with self._lock:
                self._error = "PORT BUSY"
            self._port = None
            return

        try:
            reg = self._at(ser, "AT+CEREG?")
            rssi = self._at(ser, "AT+CSQ")
            oper = self._at(ser, "AT+COPS?")
            addr = self._at(ser, "AT+CGPADDR")
        except Exception:
            with self._lock:
                self._error = "PORT BUSY"
            self._port = None
            try:
                ser.close()
            except Exception:
                pass
            return
        ser.close()

        with self._lock:
            self._error = ""

            cereg_line = self._find_prefix(reg, "+CEREG:")
            self._registered = any(f"0,{s}" in cereg_line for s in ("1", "5"))

            try:
                csq_line = self._find_prefix(rssi, "+CSQ:")
                csq_val = int(csq_line.split(":")[1].split(",")[0].strip())
                if 0 <= csq_val <= 31:
                    self._rssi_dbm = -113 + csq_val * 2
                else:
                    self._rssi_dbm = -999
            except Exception:
                self._rssi_dbm = -999

            try:
                cops_line = self._find_prefix(oper, "+COPS:")
                parts = cops_line.split('"')
                self._operator = parts[1] if len(parts) >= 2 else ""
            except Exception:
                self._operator = ""

            try:
                addr_line = self._find_prefix(addr, "+CGPADDR:")
                parts = addr_line.split('"')
                self._ip = parts[1] if len(parts) >= 2 else ""
            except Exception:
                self._ip = ""

    def _teardown(self):
        try:
            import serial
        except ImportError:
            return
        port = self._port or _find_at_port()
        if not port:
            return
        try:
            ser = serial.Serial(port, BAUD, timeout=1)
            self._at(ser, "AT%NETDEVCTL=0,1")
            ser.close()
        except Exception:
            pass
        with self._lock:
            self._registered = False
            self._rssi_dbm = -999
            self._ip = ""
            self._operator = ""

    @staticmethod
    def _find_prefix(response: str, prefix: str) -> str:
        """Find the line in a multi-line AT response that starts with prefix."""
        for line in response.splitlines():
            if line.strip().startswith(prefix):
                return line.strip()
        return ""

    @staticmethod
    def _at(ser, cmd, timeout=2.0):
        """Send AT command, read until OK/ERROR, return the full response."""
        ser.reset_input_buffer()
        ser.write((cmd + "\r\n").encode())
        lines = []
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            raw = ser.readline()
            if not raw:
                continue
            line = raw.decode(errors="replace").strip()
            if not line:
                continue
            lines.append(line)
            if line in ("OK", "ERROR") or line.startswith("+CME ERROR"):
                break
        return "\n".join(lines)
