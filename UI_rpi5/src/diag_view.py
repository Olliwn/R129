"""
R129 Driver UI -- Diagnostics View
Tesla-style split-pane: system list on left, fault code details on right.
All text rendered in dot-matrix style for consistent retro aesthetic.
"""

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter

import theme
from dot_matrix import draw_dot_text, dot_line_height
from split_pane_view import SplitPaneView

_SYSTEMS = [
    {
        "name": "EZL / Ignition",
        "pin": "Pin 8",
        "codes": [
            {"code": 17, "desc": "CPS signal missing", "active": True},
        ],
    },
    {
        "name": "ADS (N51)",
        "pin": "Pin 9",
        "codes": [],
    },
    {
        "name": "RST / Soft Top",
        "pin": "Pin 10",
        "codes": [
            {"code": 20, "desc": "Hardtop detected", "active": True},
            {"code": 28, "desc": "Speed signal missing", "active": True},
            {"code": 29, "desc": "ABS speed missing", "active": True},
        ],
    },
    {
        "name": "ATA / Alarm",
        "pin": "Pin 11",
        "codes": [
            {"code": 0, "desc": "Module unresponsive", "active": True},
        ],
    },
    {
        "name": "IRCL",
        "pin": "Pin 12",
        "codes": [],
    },
    {
        "name": "ESMC / Seats",
        "pin": "Pin 14",
        "codes": [],
    },
]


class DiagView(SplitPaneView):
    def __init__(self):
        super().__init__()
        self._items = ["EZL", "ADS", "RST", "ATA", "IRCL", "ESMC"]

    def _draw_detail(self, p: QPainter, rect: QRectF, index: int):
        if index < 0 or index >= len(_SYSTEMS):
            return
        sys_info = _SYSTEMS[index]
        self._detail_count = max(1, len(sys_info["codes"]))
        x0, y0 = rect.x(), rect.y()

        lh = dot_line_height()
        y = y0

        draw_dot_text(p, x0, y, sys_info['pin'], on_color=theme.AMBER_DIM)
        y += lh + 4

        codes = sys_info["codes"]
        n_active = sum(1 for c in codes if c["active"])

        if codes:
            draw_dot_text(p, x0, y, f"{n_active} ACTIVE CODES")
            y += lh + 8
            for i, c in enumerate(codes):
                is_sel = (self._focus == "detail" and i == self._detail_selected)
                on_color = theme.AMBER if is_sel else theme.DOT_ON
                status = "ACTIVE" if c["active"] else "STORED"
                code_top = y
                draw_dot_text(p, x0, y, f"CODE {c['code']:02d}", on_color=on_color)
                y += lh
                draw_dot_text(p, x0 + 14, y, c["desc"].upper(),
                              on_color=theme.AMBER_DIM)
                y += lh
                draw_dot_text(p, x0 + 14, y, f"({status})",
                              on_color=theme.AMBER_DIM)
                y += lh + 8
                self._register_detail_item(
                    i, QRectF(x0, code_top, rect.width(), y - code_top))
        else:
            draw_dot_text(p, x0, y, "NO FAULTS", on_color=theme.GREEN)
