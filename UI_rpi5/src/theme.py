"""
R129 Driver UI -- Theme
Shared color definitions, font helpers, and constants.
Colors are factory-accurate based on night-illuminated R129 cluster reference photos:
white/warm-white markings, amber needles, charcoal gauge faces.

Font sizes are scaled for a 5.5" 1920x1080 AMOLED viewed at ~1m distance.
Gauge views use gauge_font() which is unscaled (sizes relative to gauge radius).
"""

from PyQt5.QtGui import QColor, QFont
import os
import sys
import time

# ── UI style (retro dot-matrix vs modern clean) ─────────────────────
ui_style = "retro"

# ── Retro display imperfections ─────────────────────────────────────
retro_fx = True

GLOW_BLEED_ALPHA = 0.12
FLICKER_DIM = 0.94
FLICKER_PERIOD = 90


def is_flicker_frame() -> bool:
    """True for ~1 frame out of FLICKER_PERIOD (~3 sec at 30fps)."""
    if not retro_fx:
        return False
    return int(time.time() * 30) % FLICKER_PERIOD < 1

# ── Background ────────────────────────────────────────────────────────
BG = QColor(5, 5, 8)
GAUGE_FACE = QColor(18, 18, 22)

# ── Gauge markings (factory-accurate warm white) ─────────────────────
TICK_WHITE = QColor(230, 225, 210)
TICK_DIM = QColor(100, 98, 90)

# ── Needles ──────────────────────────────────────────────────────────
NEEDLE_AMBER = QColor(255, 160, 30)
NEEDLE_RED = QColor(200, 40, 30)

# ── Bezel rings ──────────────────────────────────────────────────────
BEZEL_HIGHLIGHT = QColor(80, 78, 72)
BEZEL_DARK = QColor(30, 28, 25)

# ── UI accent colors ─────────────────────────────────────────────────
AMBER = QColor(255, 160, 30)
AMBER_DIM = QColor(140, 80, 10)
AMBER_DARK = QColor(60, 35, 5)
GREEN = QColor(60, 200, 80)

# ── Home view vector graphics ────────────────────────────────────────
VECTOR_GREEN = QColor(0, 255, 80)

# ── Sidebar ──────────────────────────────────────────────────────────
SIDEBAR_BG = QColor(10, 10, 14)
SIDEBAR_SEPARATOR = QColor(40, 38, 34)
SIDEBAR_WIDTH = 128

# ── Dot-matrix LCD ───────────────────────────────────────────────────
DOT_ON = QColor(255, 160, 30)
DOT_OFF = QColor(25, 20, 12)
DOT_BG = QColor(12, 10, 8)
DOT_SCALE = 1.4

# ── Google Maps ───────────────────────────────────────────────────────
MAPS_API_KEY = os.environ.get("MAPS_API_KEY", "")
MAPS_DEFAULT_LAT = 60.17
MAPS_DEFAULT_LNG = 24.94

# ── Fonts ─────────────────────────────────────────────────────────────
_IS_MAC = sys.platform == "darwin"
FONT_FAMILY = "Helvetica Neue" if _IS_MAC else "DejaVu Sans"
MONO_FAMILY = "Menlo" if _IS_MAC else "DejaVu Sans Mono"

_FONT_SCALE = 1.0 if _IS_MAC else 3.2


def font(size: int, bold: bool = False) -> QFont:
    """Scaled font for UI text (menus, overlays, labels). 3.2x on RPi."""
    return QFont(FONT_FAMILY, int(size * _FONT_SCALE),
                 QFont.Bold if bold else QFont.Normal)


def mono_font(size: int, bold: bool = False) -> QFont:
    """Scaled monospace font for UI text. 3.2x on RPi."""
    return QFont(MONO_FAMILY, int(size * _FONT_SCALE),
                 QFont.Bold if bold else QFont.Normal)


def gauge_font(size: int, bold: bool = False) -> QFont:
    """Unscaled font for gauge tick labels and numbers. Size is in raw pt,
    caller must size proportionally to the gauge radius."""
    return QFont(FONT_FAMILY, size, QFont.Bold if bold else QFont.Normal)
