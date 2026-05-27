"""
R129 Driver UI -- Main Window
Fullscreen container: Sidebar | (StatusBar / ViewStack).
8 pages: Home, Classic, Modern, Diag, Settings, CarPlay, Map, Exit.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer

from input_manager import InputManager
from vehicle_state import VehicleState
from sim_provider import SimulatedProvider
from view_manager import ViewManager
from sidebar import Sidebar
from status_bar import StatusBar
from modem_state import ModemState
from audio_controller import AudioController
from home_view import HomeView
from classic_cluster_view import ClassicClusterView
from gauge_view import GaugeView
from diag_view import DiagView
from settings_view import SettingsView
from placeholder_view import PlaceholderView
from carplay_view import CarPlayView
from exit_view import ExitView
from map_view import MapView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self._state = VehicleState(self)
        self._modem = ModemState(self)
        self._provider = SimulatedProvider(self._state, self)
        self._audio = AudioController(self)

        container = QWidget()
        outer = QHBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._sidebar = Sidebar(page_count=8, audio=self._audio)
        outer.addWidget(self._sidebar)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self._status_bar = StatusBar(self._state, modem=self._modem)
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
        self._view_mgr.add_view("SETTINGS", SettingsView(modem=self._modem))
        self._carplay_view = CarPlayView()
        self._view_mgr.add_view("CARPLAY", self._carplay_view)
        self._carplay_index = self._view_mgr.count - 1
        self._view_mgr.add_view("MAP", MapView())
        self._view_mgr.add_view("EXIT", ExitView())
        self._view_mgr.switch_to(0)

        self._view_mgr.view_changed.connect(
            lambda idx, name: self._status_bar.set_page_name(name))

        # Volume taps on the sidebar steal Wayland focus from LIVI, which
        # otherwise pushes the CarPlay placeholder forward. Re-raise LIVI
        # shortly after a volume nudge while CarPlay is the active page.
        self._sidebar.volume_touched.connect(self._restore_livi_if_carplay)

        # Long-press the CarPlay sidebar icon (`theme.TOUCH_HOLD_MS`) →
        # stop LIVI. The CarPlay overlay is full-bleed inside
        # x ≥ SIDEBAR_WIDTH, so the sidebar slot is the only
        # always-tappable place to put this control. Stop is idempotent
        # — safe even when LIVI isn't running.
        self._sidebar.carplay_stop_requested.connect(self._stop_carplay)

        self._input = InputManager(self)
        self._input.action_triggered.connect(self._view_mgr.handle_action)

    def _stop_carplay(self):
        """Stop the LIVI CarPlay process. Fired by a long-press on the
        CarPlay sidebar icon. Works from any page and is idempotent."""
        self._carplay_view._stop_livi()

    def _restore_livi_if_carplay(self):
        """Re-raise the main LIVI window after a sidebar volume tap.

        With the labwc rule pinning the main LIVI top-level to the
        always-on-top layer, the Qt surface should never cover it on a
        sidebar tap. A single immediate refocus is kept as a safety net for
        first-tap-after-launch when the layer assignment may not yet be in
        effect."""
        if self._view_mgr.current_index != self._carplay_index:
            return
        if not self._carplay_view.livi_running:
            return
        self._carplay_view._focus_livi()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        self._carplay_view.shutdown()
        super().closeEvent(event)
