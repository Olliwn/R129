"""
R129 Driver UI -- View Manager
4-state navigation model:

  SIDEBAR  -- sidebar has focus, UP/DOWN select page, PRESS/RIGHT activates
  PAGE     -- page has focus (display-only pages stay here)
  MENU     -- inside a menu page's item list
  PARAM    -- editing a parameter value

LONG_PRESS always returns to SIDEBAR from any state.
"""

from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import QObject, pyqtSignal

from input_actions import InputAction
from sidebar import Sidebar


class ViewManager(QObject):
    view_changed = pyqtSignal(int, str)
    state_changed = pyqtSignal(str)  # "sidebar", "page", "menu", "param"

    def __init__(self, stack: QStackedWidget, sidebar: Sidebar, parent=None):
        super().__init__(parent)
        self._stack = stack
        self._sidebar = sidebar
        self._names: list[str] = []
        self._state = "sidebar"

        self._sidebar.page_activated.connect(self._on_sidebar_touch)

    def add_view(self, name: str, widget: QWidget):
        self._stack.addWidget(widget)
        self._names.append(name)

    @property
    def current_index(self) -> int:
        return self._stack.currentIndex()

    @property
    def count(self) -> int:
        return self._stack.count()

    @property
    def nav_state(self) -> str:
        return self._state

    def switch_to(self, index: int):
        if 0 <= index < self._stack.count():
            self._stack.setCurrentIndex(index)
            self._sidebar.set_selected(index)
            self.view_changed.emit(index, self._names[index])

    def _set_state(self, new_state: str):
        if self._state != new_state:
            self._state = new_state
            self._sidebar.set_bright(new_state == "sidebar")
            self.state_changed.emit(new_state)

    def _on_sidebar_touch(self, index: int):
        self.switch_to(index)
        self._set_state("page")

    def _go_sidebar(self):
        self._set_state("sidebar")

    def _activate_page(self):
        self.switch_to(self._sidebar.selected)
        self._set_state("page")

    # ── Central input dispatch ───────────────────────────────────────

    def handle_action(self, action: InputAction):
        if action == InputAction.LONG_PRESS:
            self._go_sidebar()
            return

        if self._state == "sidebar":
            self._handle_sidebar(action)
        else:
            self._handle_page(action)

    def _handle_sidebar(self, action: InputAction):
        if action in (InputAction.UP, InputAction.CCW):
            self._sidebar.move_selection(-1)
            self._preview_selected()
        elif action in (InputAction.DOWN, InputAction.CW):
            self._sidebar.move_selection(1)
            self._preview_selected()
        elif action in (InputAction.PRESS, InputAction.RIGHT):
            self._activate_page()

    def _preview_selected(self):
        """Show the selected page as a live preview while browsing the sidebar."""
        idx = self._sidebar.selected
        if 0 <= idx < self._stack.count():
            self._stack.setCurrentIndex(idx)
            self.view_changed.emit(idx, self._names[idx])

    def _handle_page(self, action: InputAction):
        widget = self._stack.currentWidget()
        if hasattr(widget, "handle_input"):
            result = widget.handle_input(action)
            if result == "back":
                self._go_sidebar()
