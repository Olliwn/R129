"""
R129 Driver UI -- Audio Controller

Single source of truth for system audio volume. Wraps PipeWire's `wpctl`
command-line tool for get / set / nudge operations on `@DEFAULT_AUDIO_SINK@`.

Behaviour:
  - Polls the system volume once per second so the UI tracks external
    changes (Bluetooth A2DP absolute-volume from the iPhone, CarPlay
    control messages from LIVI, manual `wpctl` commands from SSH, etc).
  - Emits `volume_changed(float)` whenever the system volume actually
    changes by more than `MIN_DELTA_FOR_SIGNAL` (avoids redundant repaints).
  - Gracefully no-ops on hosts without `wpctl` in PATH (macOS dev), so the
    same module can be imported from a dev laptop without crashing.

The Pi-side bring-up procedure (`work/audio_tuning/in_car_pi_bringup_procedure.md`)
expects the default sink to be capped at 50% (-6 dB) at boot — set by
`~/bin/audio-safe.sh`. This module respects whatever the current sink volume
is; it does not impose its own cap.
"""

import shutil
import subprocess

from PyQt5.QtCore import QObject, QTimer, pyqtSignal


POLL_INTERVAL_MS = 1000
NUDGE_STEP = 0.05            # 5% per ▲ / ▼ tap or CW / CCW step
MIN_DELTA_FOR_SIGNAL = 0.005


class AudioController(QObject):
    """PipeWire/wpctl-backed system volume controller.

    Owned by MainWindow; lives for the duration of the application.
    """

    volume_changed = pyqtSignal(float)   # 0.0 ..= 1.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._volume = 0.5
        self._available = shutil.which("wpctl") is not None

        self._poll = QTimer(self)
        self._poll.timeout.connect(self._sync)
        self._poll.start(POLL_INTERVAL_MS)
        QTimer.singleShot(0, self._sync)

    # ── public API ───────────────────────────────────────────────────

    @property
    def volume(self) -> float:
        return self._volume

    @property
    def available(self) -> bool:
        return self._available

    def set_volume(self, v: float):
        v = max(0.0, min(1.0, float(v)))
        if self._available:
            try:
                subprocess.run(
                    ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{v:.2f}"],
                    timeout=2, check=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass
        self._update(v)

    def nudge_up(self):
        self.set_volume(self._volume + NUDGE_STEP)

    def nudge_down(self):
        self.set_volume(self._volume - NUDGE_STEP)

    # ── internals ────────────────────────────────────────────────────

    def _sync(self):
        if not self._available:
            return
        try:
            out = subprocess.check_output(
                ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"],
                timeout=1, text=True, stderr=subprocess.DEVNULL,
            )
            # wpctl output looks like "Volume: 0.50" or "Volume: 0.50 [MUTED]"
            for tok in out.split():
                try:
                    v = float(tok)
                    self._update(v)
                    return
                except ValueError:
                    continue
        except Exception:
            pass

    def _update(self, v: float):
        if abs(v - self._volume) >= MIN_DELTA_FOR_SIGNAL:
            self._volume = v
            self.volume_changed.emit(v)
