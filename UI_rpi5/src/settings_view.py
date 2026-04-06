"""
R129 Driver UI -- Settings View
Tesla-style split-pane: category list on left, options on right.
Supports param editing (brightness bar, etc.) via CW/CCW.
All text rendered in dot-matrix style for consistent retro aesthetic.
"""

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush

import theme
from dot_matrix import draw_dot_text, dot_line_height
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


class SettingsView(SplitPaneView):
    def __init__(self):
        super().__init__()
        self._items = ["Display", "Audio", "BT", "Input", "System", "About"]

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
        cat = _CATEGORIES[index]
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
            draw_dot_text(p, x0 + 14, y, val_str,
                          on_color=theme.AMBER if is_sel else theme.AMBER_DIM)
            y += lh

            if self._focus == "param" and is_sel and opt["type"] == "slider":
                self._draw_param_bar(p, x0, y + 4, rw * 0.6, 14,
                                     self._param_value, self._param_min, self._param_max)
                y += 30

            y += 4

    def _format_value(self, opt) -> str:
        if opt["key"] == "UI Style":
            return theme.ui_style.upper()
        if opt["key"] == "Retro FX":
            return "ON" if theme.retro_fx else "OFF"
        v = opt["value"]
        if opt["type"] == "slider":
            return f"{v}{opt.get('unit', '')}"
        return str(v) if v else "---"

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
