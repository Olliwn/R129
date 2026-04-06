"""
R129 Driver UI -- Input Action Definitions
Unified enum for all physical inputs: joystick, rotary encoder, push button.
"""

from enum import Enum, auto


class InputAction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CW = auto()          # encoder clockwise
    CCW = auto()         # encoder counter-clockwise
    PRESS = auto()       # push button short press (select/confirm)
    LONG_PRESS = auto()  # push button held >600ms (back to home/gauges)
