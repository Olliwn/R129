"""
R129 Driver UI -- CarPlay View
Launches LIVI as a Wayland subprocess positioned beside the sidebar.
labwc window rule places LIVI at x=SIDEBAR_WIDTH, keeping the sidebar visible.
Navigating away minimizes the LIVI window (process stays alive, phone stays
paired). Returning restores focus. Touch or PRESS launches LIVI.
"""

import os
import signal
import subprocess

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

import theme
from dot_matrix import draw_dot_text, dot_line_height
from input_actions import InputAction

LIVI_PATH = "/home/pi/LIVI/LIVI.AppImage"
LIVI_APP_ID = "livi"
# LIVI can spawn auxiliary top-levels (e.g. "USB Permission Required"). For
# focus operations we must target the main CarPlay top-level by title so the
# Qt sidebar's volume taps don't accidentally re-raise a hidden modal.
LIVI_MAIN_TITLE = "LIVI"
DONGLE_VID_PID = "1314:1520"
DONGLE_CHECK_INTERVAL = 5000


class CarPlayView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._proc: subprocess.Popen | None = None
        self._dongle_present: bool | None = None  # None = never checked

        self._status_timer = QTimer(self)
        self._status_timer.timeout.connect(self._poll_status)
        self._status_timer.start(DONGLE_CHECK_INTERVAL)
        QTimer.singleShot(200, self._poll_status)

    @property
    def livi_running(self) -> bool:
        if self._proc is None:
            return False
        return self._proc.poll() is None

    # ── Input handling ───────────────────────────────────────────────

    def handle_input(self, action: InputAction):
        if action == InputAction.PRESS:
            if self.livi_running:
                self._focus_livi()
            else:
                self._launch_livi()
            return True
        if action == InputAction.LEFT:
            return "back"
        return False

    def mousePressEvent(self, event):
        if self.livi_running:
            self._focus_livi()
        else:
            self._launch_livi()

    def on_shown(self):
        """Called by ViewManager when this view becomes visible."""
        if self.livi_running:
            self._focus_livi()

    def on_hidden(self):
        """Called by ViewManager when navigating away from this view.
        LIVI process stays alive so the phone connection is preserved;
        we only minimize the window so the other page is visible."""
        if self.livi_running:
            self._minimize_livi()

    def shutdown(self):
        """Called on app exit to stop LIVI cleanly."""
        self._stop_livi()

    # ── LIVI process lifecycle ───────────────────────────────────────

    def _launch_livi(self):
        if self.livi_running:
            return
        if not os.path.isfile(LIVI_PATH):
            return

        env = os.environ.copy()
        env["WAYLAND_DISPLAY"] = "wayland-0"
        env["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"
        env["XDG_SESSION_TYPE"] = "wayland"

        self._proc = subprocess.Popen(
            [LIVI_PATH, "--no-sandbox"],
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.update()

    def _stop_livi(self):
        if self._proc is None:
            return
        try:
            pgid = os.getpgid(self._proc.pid)
            os.killpg(pgid, signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass
        try:
            self._proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                pgid = os.getpgid(self._proc.pid)
                os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, OSError):
                pass
        self._proc = None
        self.update()

    # ── Window visibility via wlrctl ─────────────────────────────────

    def _wlrctl(self, *args) -> bool:
        """Fire-and-forget wlrctl invocation.

        Uses Popen instead of subprocess.run so the Qt event loop is never
        blocked. The focus race against the compositor is short (single-digit
        ms), and we issue several focus attempts in quick succession from
        MainWindow; blocking on each one would queue up and stall subsequent
        touch events (occasionally swallowing the next volume tap)."""
        try:
            subprocess.Popen(
                ["wlrctl", "window", *args],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except FileNotFoundError:
            return False

    def _minimize_livi(self):
        # Minimize every LIVI top-level (main + auxiliary dialogs) when the
        # user navigates away from the CarPlay page.
        self._wlrctl("minimize", f"app_id:{LIVI_APP_ID}")

    def _focus_livi(self):
        # Only re-focus the main CarPlay window — never an auxiliary modal.
        self._wlrctl("focus", f"title:{LIVI_MAIN_TITLE}")

    # ── Dongle detection ─────────────────────────────────────────────

    def _poll_status(self):
        prev = self._dongle_present
        try:
            with open("/sys/bus/usb/devices/3-1/idVendor") as f:
                self._dongle_present = f.read().strip() == "1314"
        except OSError:
            self._dongle_present = self._check_lsusb()
        if self._dongle_present != prev:
            self.update()

    def _check_lsusb(self) -> bool:
        try:
            out = subprocess.check_output(
                ["lsusb", "-d", DONGLE_VID_PID],
                timeout=2, text=True, stderr=subprocess.DEVNULL,
            )
            return len(out.strip()) > 0
        except Exception:
            return False

    # ── Paint ────────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillRect(self.rect(), theme.BG)

        w, h = self.width(), self.height()
        lh = dot_line_height()
        cx = w * 0.08
        cy = h * 0.20

        draw_dot_text(p, cx, cy, "CARPLAY")
        cy += lh * 1.8

        if self.livi_running:
            draw_dot_text(p, cx, cy, "LIVI ACTIVE",
                          on_color=theme.GREEN)
            cy += lh * 1.5
            draw_dot_text(p, cx, cy, "TAP TO SHOW",
                          on_color=theme.AMBER_DIM)
        else:
            if self._dongle_present:
                draw_dot_text(p, cx, cy, "DONGLE CONNECTED",
                              on_color=theme.GREEN)
            elif self._dongle_present is None:
                draw_dot_text(p, cx, cy, "CHECKING DONGLE...",
                              on_color=theme.AMBER_DIM)
            else:
                draw_dot_text(p, cx, cy, "DONGLE NOT FOUND",
                              on_color=theme.NEEDLE_RED)
            cy += lh * 1.5
            draw_dot_text(p, cx, cy, "TAP OR PRESS TO LAUNCH",
                          on_color=theme.AMBER_DIM)

        p.end()
