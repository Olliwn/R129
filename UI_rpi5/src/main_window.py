"""
R129 Driver UI -- Main Window
Fullscreen container: Sidebar | (StatusBar / ViewStack).
8 pages: Home, Classic, Modern, Diag, Settings, Media, Map, Spare.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout,
)
from PyQt5.QtCore import Qt

from input_manager import InputManager
from vehicle_state import VehicleState
from sim_provider import SimulatedProvider
from view_manager import ViewManager
from sidebar import Sidebar
from status_bar import StatusBar
from home_view import HomeView
from classic_cluster_view import ClassicClusterView
from gauge_view import GaugeView
from diag_view import DiagView
from settings_view import SettingsView
from placeholder_view import PlaceholderView
from map_view import MapView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self._state = VehicleState(self)
        self._provider = SimulatedProvider(self._state, self)

        container = QWidget()
        outer = QHBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._sidebar = Sidebar(page_count=8)
        outer.addWidget(self._sidebar)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self._status_bar = StatusBar(self._state)
        self._status_bar.setMinimumHeight(StatusBar.HEIGHT)
        self._status_bar.setMaximumHeight(StatusBar.HEIGHT)
        right_layout.addWidget(self._status_bar, 0)

        stack = QStackedWidget()
        right_layout.addWidget(stack, 1)
        outer.addWidget(right_panel)

        self.setCentralWidget(container)

        self._view_mgr = ViewManager(stack, self._sidebar, self)
        self._view_mgr.add_view("HOME", HomeView(self._state))
        self._view_mgr.add_view("CLASSIC", ClassicClusterView(self._state))
        self._view_mgr.add_view("MODERN", GaugeView(self._state))
        self._view_mgr.add_view("DIAG", DiagView())
        self._view_mgr.add_view("SETTINGS", SettingsView())
        self._view_mgr.add_view("MEDIA", PlaceholderView("MEDIA"))
        self._view_mgr.add_view("MAP", MapView())
        self._view_mgr.add_view("SPARE", PlaceholderView("SYSTEM INFO"))
        self._view_mgr.switch_to(0)

        self._view_mgr.view_changed.connect(
            lambda idx, name: self._status_bar.set_page_name(name))

        self._input = InputManager(self)
        self._input.action_triggered.connect(self._view_mgr.handle_action)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        super().keyPressEvent(event)
