"""
R129 Driver UI -- Settings View
Tesla-style split-pane: category list on left, options on right.
Supports param editing (brightness bar, etc.) via CW/CCW.
All text rendered in dot-matrix style for consistent retro aesthetic.
"""

from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush

import theme
from dot_matrix import draw_dot_text, dot_line_height, dot_text_width
from split_pane_view import SplitPaneView

_CATEGORIES = [
    {
        "name": "Display",
        "options": [
            {"key": "Brightness", "value": 80, "type": "slider", "min": 0, "max": 100, "unit": "%"},
            {"key": "Auto-dim", "value": "On", "type": "toggle"},
            {"key": "UI Style", "value": None, "type": "toggle"},
            {"key": "Retro FX", "value": None, "type": "toggle"},
            {"key": "Color scheme", "value": "Classic amber", "type": "text"},
        ],
    },
    {
        "name": "LTE",
        "options": [
            {"key": "LTE", "value": None, "type": "toggle"},
            {"key": "Status", "value": "", "type": "modem_info"},
            {"key": "Operator", "value": "", "type": "modem_info"},
            {"key": "Signal", "value": "", "type": "modem_info"},
            {"key": "IP address", "value": "", "type": "modem_info"},
        ],
    },
    {
        "name": "Audio / DSP",
        "options": [
            {"key": "DSP Preset", "value": "Flat", "type": "text"},
            {"key": "Volume limit", "value": 85, "type": "slider", "min": 0, "max": 100, "unit": "%"},
            {"key": "CarPlay audio", "value": "Enabled", "type": "text"},
        ],
    },
    {
        "name": "Bluetooth",
        "options": [
            {"key": "BLE status", "value": "Connected", "type": "text"},
            {"key": "Device name", "value": "R129-Hub", "type": "text"},
            {"key": "Auto reconnect", "value": "On", "type": "toggle"},
        ],
    },
    {
        "name": "Input",
        "options": [
            {"key": "Encoder sensitivity", "value": "Medium", "type": "text"},
            {"key": "Long-press delay", "value": "600ms", "type": "text"},
            {"key": "Haptic feedback", "value": "Off", "type": "toggle"},
        ],
    },
    {
        "name": "System",
        "options": [
            {"key": "Boot animation", "value": "Wireframe", "type": "text"},
            {"key": "Uptime", "value": "", "type": "text"},
            {"key": "Software version", "value": "0.2.0-dev", "type": "text"},
        ],
    },
    {
        "name": "About",
        "options": [
            {"key": "Vehicle", "value": "R129 500 SL (1993)", "type": "text"},
            {"key": "VIN", "value": "WDB1290...", "type": "text"},
            {"key": "Project", "value": "github.com/.../R129", "type": "text"},
        ],
    },
]

_LTE_INDEX = 1


class SettingsView(SplitPaneView):
    def __init__(self, modem=None):
        super().__init__()
        self._modem = modem
        self._items = ["Display", "LTE", "Audio", "BT", "Input", "System", "About"]

        if modem:
            modem.state_changed.connect(self._on_modem_changed)
            self._refresh_timer = QTimer(self)
            self._refresh_timer.timeout.connect(self._on_modem_changed)
            self._refresh_timer.start(5000)

    def _on_modem_changed(self):
        if self._selected == _LTE_INDEX:
            self.update()

    def _get_options(self, index: int):
        if index < 0 or index >= len(_CATEGORIES):
            return []
        return _CATEGORIES[index]["options"]

    def _on_detail_press(self, detail_index: int):
        opts = self._get_options(self._selected)
        if detail_index < 0 or detail_index >= len(opts):
            return
        opt = opts[detail_index]

        if opt["type"] == "slider":
            self.start_param_edit(opt["key"], opt["value"],
                                  opt.get("min", 0), opt.get("max", 100))
        elif opt["type"] == "toggle":
            if opt["key"] == "UI Style":
                theme.ui_style = "modern" if theme.ui_style == "retro" else "retro"
            elif opt["key"] == "Retro FX":
                theme.retro_fx = not theme.retro_fx
            elif opt["key"] == "LTE":
                if self._modem:
                    self._modem.set_enabled(not self._modem.enabled)
            elif opt["value"] in ("On", "Off"):
                opt["value"] = "Off" if opt["value"] == "On" else "On"
            self.update()

    def _on_param_done(self, key: str, value: int, cancelled: bool):
        if cancelled:
            return
        opts = self._get_options(self._selected)
        for opt in opts:
            if opt["key"] == key:
                opt["value"] = value
                break
        self.update()

    def _draw_detail(self, p: QPainter, rect: QRectF, index: int):
        if index < 0 or index >= len(_CATEGORIES):
            return
        opts = self._get_options(index)
        self._detail_count = len(opts)

        x0, y0 = rect.x(), rect.y()
        rw = rect.width()
        lh = dot_line_height()
        y = y0

        for i, opt in enumerate(opts):
            is_sel = (self._focus in ("detail", "param") and i == self._detail_selected)
            on_color = theme.AMBER if is_sel else theme.DOT_ON

            draw_dot_text(p, x0, y, opt["key"], on_color=on_color)
            y += lh

            val_str = self._format_value(opt)
            val_color = self._value_color(opt, is_sel)
            draw_dot_text(p, x0 + 14, y, val_str, on_color=val_color)
            y += lh

            if self._focus == "param" and is_sel and opt["type"] == "slider":
                self._draw_param_bar(p, x0, y + 4, rw * 0.6, 14,
                                     self._param_value, self._param_min, self._param_max)
                y += 30

            y += 4

    def _value_color(self, opt, is_sel):
        if opt["type"] == "modem_info" and self._modem:
            if opt["key"] == "Status":
                return theme.GREEN if self._modem.registered else theme.NEEDLE_RED
        return theme.AMBER if is_sel else theme.AMBER_DIM

    def _format_value(self, opt) -> str:
        if opt["key"] == "UI Style":
            return theme.ui_style.upper()
        if opt["key"] == "Retro FX":
            return "ON" if theme.retro_fx else "OFF"
        if opt["key"] == "LTE":
            if self._modem:
                return "ON" if self._modem.enabled else "OFF"
            return "N/A"
        if opt["type"] == "modem_info":
            return self._modem_value(opt["key"])
        v = opt["value"]
        if opt["type"] == "slider":
            return f"{v}{opt.get('unit', '')}"
        return str(v) if v else "---"

    def _modem_value(self, key: str) -> str:
        if not self._modem:
            return "N/A"
        m = self._modem
        if key == "Status":
            if not m.enabled:
                return "DISABLED"
            if m.error:
                return m.error
            return "REGISTERED" if m.registered else "SEARCHING"
        if key == "Operator":
            return m.operator or "---"
        if key == "Signal":
            dbm = m.rssi_dbm
            bars = m.rssi_bars
            if dbm == -999:
                return "---"
            bar_str = "|" * bars + "." * (4 - bars)
            return f"{dbm}DBM  {bar_str}"
        if key == "IP address":
            return m.ip or "---"
        return "---"

    def _draw_param_bar(self, p, x, y, w, h, value, min_v, max_v):
        p.setPen(QPen(theme.AMBER_DARK, 1))
        p.setBrush(theme.BG)
        p.drawRect(QRectF(x, y, w, h))

        frac = max(0.0, min(1.0, (value - min_v) / (max_v - min_v)))
        fill_w = (w - 4) * frac
        if fill_w > 0:
            p.setPen(Qt.NoPen)
            p.setBrush(theme.AMBER)
            p.drawRect(QRectF(x + 2, y + 2, fill_w, h - 4))
