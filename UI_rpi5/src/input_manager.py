"""
R129 Driver UI -- Input Manager
Translates physical inputs (GPIO joystick/encoder on RPi5, keyboard on desktop)
into InputAction signals consumed by the view layer.

On RPi5: uses gpiozero Button + RotaryEncoder with lgpio backend.
On macOS/desktop: maps keyboard keys to the same actions for development.
"""

import sys
import time

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QApplication

from input_actions import InputAction

# GPIO pin assignments -- Alps RKJXT1F42001 via CAT6 umbilical
GPIO_JOY_UP = 17
GPIO_JOY_DOWN = 27
GPIO_JOY_LEFT = 22
GPIO_JOY_RIGHT = 23
GPIO_ENC_A = 24
GPIO_ENC_B = 25
GPIO_PUSH = 5

LONG_PRESS_MS = 600
DEBOUNCE_S = 0.05  # 50ms software debounce for joystick buttons

# Keyboard mapping for desktop development
_KEY_MAP = {
    Qt.Key_Up: InputAction.UP,
    Qt.Key_Down: InputAction.DOWN,
    Qt.Key_Left: InputAction.LEFT,
    Qt.Key_Right: InputAction.RIGHT,
    Qt.Key_PageUp: InputAction.CW,
    Qt.Key_PageDown: InputAction.CCW,
    Qt.Key_Return: InputAction.PRESS,
    Qt.Key_Enter: InputAction.PRESS,
}


def _is_rpi() -> bool:
    """Detect Raspberry Pi by checking for /proc/device-tree/model."""
    try:
        with open("/proc/device-tree/model", "r") as f:
            return "raspberry pi" in f.read().lower()
    except OSError:
        return False


class InputManager(QObject):
    """Unified input source. Emits ``action_triggered`` for every discrete input event."""

    action_triggered = pyqtSignal(InputAction)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._push_down_time: float = 0.0
        self._long_press_fired: bool = False
        self._long_press_timer = QTimer(self)
        self._long_press_timer.setSingleShot(True)
        self._long_press_timer.setInterval(LONG_PRESS_MS)
        self._long_press_timer.timeout.connect(self._on_long_press_timeout)

        self._init_keyboard()

        if _is_rpi():
            self._init_gpio()

    # ── GPIO backend (RPi5) ───────────────────────────────────────────

    def _init_gpio(self):
        try:
            from gpiozero import Button, RotaryEncoder
        except Exception as exc:
            print(f"[InputManager] GPIO unavailable, keyboard-only mode: {exc}")
            return

        try:
            self._buttons = {
                InputAction.UP: Button(GPIO_JOY_UP, pull_up=True, bounce_time=DEBOUNCE_S),
                InputAction.DOWN: Button(GPIO_JOY_DOWN, pull_up=True, bounce_time=DEBOUNCE_S),
                InputAction.LEFT: Button(GPIO_JOY_LEFT, pull_up=True, bounce_time=DEBOUNCE_S),
                InputAction.RIGHT: Button(GPIO_JOY_RIGHT, pull_up=True, bounce_time=DEBOUNCE_S),
            }
            for action, btn in self._buttons.items():
                btn.when_pressed = lambda a=action: self.action_triggered.emit(a)

            self._encoder = RotaryEncoder(GPIO_ENC_A, GPIO_ENC_B, max_steps=0)
            self._last_enc_steps = 0
            self._enc_poll = QTimer(self)
            self._enc_poll.timeout.connect(self._poll_encoder)
            self._enc_poll.start(20)

            self._push = Button(GPIO_PUSH, pull_up=True, bounce_time=DEBOUNCE_S)
            self._push.when_pressed = self._on_push_down
            self._push.when_released = self._on_push_up

            print("[InputManager] GPIO backend initialized")
        except Exception as exc:
            print(f"[InputManager] GPIO init failed, keyboard-only mode: {exc}")

    def _poll_encoder(self):
        steps = self._encoder.steps
        delta = steps - self._last_enc_steps
        self._last_enc_steps = steps
        if delta > 0:
            for _ in range(delta):
                self.action_triggered.emit(InputAction.CW)
        elif delta < 0:
            for _ in range(-delta):
                self.action_triggered.emit(InputAction.CCW)

    # ── Keyboard backend (desktop dev) ────────────────────────────────

    def _init_keyboard(self):
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

    def eventFilter(self, obj, event):
        from PyQt5.QtCore import QEvent

        if event.type() == QEvent.KeyPress and not event.isAutoRepeat():
            key = event.key()
            if key in _KEY_MAP:
                action = _KEY_MAP[key]
                if action == InputAction.PRESS:
                    self._on_push_down()
                else:
                    self.action_triggered.emit(action)
                return True

        if event.type() == QEvent.KeyRelease and not event.isAutoRepeat():
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self._on_push_up()
                return True

        return super().eventFilter(obj, event)

    # ── Push button logic (shared by both backends) ───────────────────

    def _on_push_down(self):
        self._push_down_time = time.monotonic()
        self._long_press_fired = False
        self._long_press_timer.start()

    def _on_push_up(self):
        self._long_press_timer.stop()
        if not self._long_press_fired:
            self.action_triggered.emit(InputAction.PRESS)

    def _on_long_press_timeout(self):
        self._long_press_fired = True
        self.action_triggered.emit(InputAction.LONG_PRESS)
