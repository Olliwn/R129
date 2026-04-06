"""
R129 Driver UI -- Map View
Slippy-tile map renderer using CartoDB dark basemap tiles.
No QWebEngineView (avoids Wayland compositor corruption on RPi5).
Joystick: CW/CCW zoom, arrows pan, PRESS toggles tile layer.
Touch: drag to pan, pinch to zoom.
"""

import math
import threading
from collections import OrderedDict
from urllib.request import urlopen, Request

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QPainter, QPixmap, QImage, QColor, QPen, QBrush
from PyQt5.QtCore import QRectF

import theme
from input_actions import InputAction

_BG = QColor(0x1A, 0x1A, 0x2E)

TILE_URLS = [
    "https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
    "https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png",
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
]
TILE_NAMES = ["DARK", "LIGHT", "OSM"]

TILE_PX = 512  # @2x tiles are 512x512 physical pixels
BTN_SIZE = 72
BTN_MARGIN = 14
MAX_CONCURRENT = 8
_fetch_sem = threading.Semaphore(MAX_CONCURRENT)


def _lng_to_tx(lng, z):
    return (lng + 180.0) / 360.0 * (1 << z)


def _lat_to_ty(lat, z):
    r = math.radians(lat)
    return (1.0 - math.log(math.tan(r) + 1.0 / math.cos(r)) / math.pi) / 2.0 * (1 << z)


def _tx_to_lng(tx, z):
    return tx / (1 << z) * 360.0 - 180.0


def _ty_to_lat(ty, z):
    n = math.pi - 2.0 * math.pi * ty / (1 << z)
    return math.degrees(math.atan(math.sinh(n)))


class _TileCache:
    def __init__(self, capacity=256):
        self._d = OrderedDict()
        self._cap = capacity

    def get(self, key):
        if key in self._d:
            self._d.move_to_end(key)
            return self._d[key]
        return None

    def put(self, key, val):
        self._d[key] = val
        self._d.move_to_end(key)
        while len(self._d) > self._cap:
            self._d.popitem(last=False)


class _MapWidget(QWidget):
    _tile_ready = pyqtSignal(int, int, int, int, bytes)  # layer, z, x, y, png

    def __init__(self):
        super().__init__()
        self._lat = theme.MAPS_DEFAULT_LAT
        self._lng = theme.MAPS_DEFAULT_LNG
        self._zoom = 13
        self._layer = 0
        self._cache = _TileCache()
        self._pending = set()

        self._home_lat = self._lat
        self._home_lng = self._lng

        self._drag_start = None
        self._drag_off = QPointF(0, 0)
        self._pinch_dist = 0.0
        self._panned = False

        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self._tile_ready.connect(self._on_tile_data)

    def _visible_tiles(self, margin=1):
        w, h = self.width(), self.height()
        if w < 1 or h < 1:
            return []
        z = self._zoom
        ox, oy = self._drag_off.x(), self._drag_off.y()
        cx = _lng_to_tx(self._lng, z) * TILE_PX
        cy = _lat_to_ty(self._lat, z) * TILE_PX
        left = cx - w / 2
        top = cy - h / 2
        n = 1 << z

        tx0 = int(math.floor(left / TILE_PX)) - margin
        tx1 = int(math.floor((left + w - 1) / TILE_PX)) + margin
        ty0 = int(math.floor(top / TILE_PX)) - margin
        ty1 = int(math.floor((top + h - 1) / TILE_PX)) + margin

        out = []
        for ty in range(max(0, ty0), min(n, ty1 + 1)):
            for tx in range(tx0, tx1 + 1):
                sx = tx * TILE_PX - left + ox
                sy = ty * TILE_PX - top + oy
                out.append((tx % n, ty, int(sx), int(sy)))
        return out

    # ---- painting ----------------------------------------------------

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), _BG)
        z = self._zoom
        layer = self._layer
        for tx, ty, sx, sy in self._visible_tiles():
            key = (layer, z, tx, ty)
            pix = self._cache.get(key)
            if pix is not None:
                p.drawPixmap(sx, sy, pix)
            elif key not in self._pending:
                self._fetch(layer, z, tx, ty)
        if self._panned:
            self._draw_recenter_btn(p)
        p.end()

    def _btn_rect(self):
        return QRectF(self.width() - BTN_SIZE - BTN_MARGIN,
                      self.height() - BTN_SIZE - BTN_MARGIN,
                      BTN_SIZE, BTN_SIZE)

    def _draw_recenter_btn(self, p):
        r = self._btn_rect()
        p.setRenderHint(QPainter.Antialiasing, False)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0, 0, 0, 140))
        p.drawRoundedRect(r, 8, 8)
        cx, cy = r.center().x(), r.center().y()
        amber = QColor(255, 180, 50, 220)
        pen = QPen(amber, 3)
        p.setPen(pen)
        arm = 18
        p.drawLine(int(cx - arm), int(cy), int(cx + arm), int(cy))
        p.drawLine(int(cx), int(cy - arm), int(cx), int(cy + arm))
        ring = 10
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(int(cx - ring), int(cy - ring), ring * 2, ring * 2)
        p.setBrush(amber)
        p.setPen(Qt.NoPen)
        p.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

    def _hit_recenter(self, x, y):
        if not self._panned:
            return False
        return self._btn_rect().contains(x, y)

    # ---- tile fetch --------------------------------------------------

    def _fetch(self, layer, z, x, y):
        key = (layer, z, x, y)
        self._pending.add(key)
        t = threading.Thread(target=self._do_fetch, args=(layer, z, x, y), daemon=True)
        t.start()

    def _do_fetch(self, layer, z, x, y):
        _fetch_sem.acquire()
        try:
            url = TILE_URLS[layer].format(z=z, x=x, y=y)
            req = Request(url, headers={"User-Agent": "R129-UI/1.0"})
            data = urlopen(req, timeout=12).read()
            self._tile_ready.emit(layer, z, x, y, data)
        except Exception as e:
            print(f"[map] tile {z}/{x}/{y}: {e}")
            self._pending.discard((layer, z, x, y))
        finally:
            _fetch_sem.release()

    def _on_tile_data(self, layer, z, x, y, data):
        img = QImage()
        img.loadFromData(data)
        if not img.isNull():
            pix = QPixmap.fromImage(img)
            if pix.width() != TILE_PX or pix.height() != TILE_PX:
                pix = pix.scaled(TILE_PX, TILE_PX, Qt.IgnoreAspectRatio,
                                 Qt.SmoothTransformation)
            self._cache.put((layer, z, x, y), pix)
        self._pending.discard((layer, z, x, y))
        self.update()

    # ---- mouse drag --------------------------------------------------

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._drag_start = ev.pos()

    def mouseMoveEvent(self, ev):
        if self._drag_start is not None:
            self._drag_off = QPointF(ev.pos() - self._drag_start)
            self.update()

    def mouseReleaseEvent(self, ev):
        if self._drag_start is not None:
            dx = ev.pos().x() - self._drag_start.x()
            dy = ev.pos().y() - self._drag_start.y()
            self._drag_start = None
            self._drag_off = QPointF(0, 0)
            if abs(dx) > 4 or abs(dy) > 4:
                self._pan_px(-dx, -dy)
            elif self._hit_recenter(ev.pos().x(), ev.pos().y()):
                self._recenter()
            else:
                self.update()

    # ---- wheel / pinch zoom ------------------------------------------

    def wheelEvent(self, ev):
        delta = ev.angleDelta().y()
        if delta > 0:
            self._zoom = min(18, self._zoom + 1)
        elif delta < 0:
            self._zoom = max(2, self._zoom - 1)
        else:
            return
        self.update()

    # ---- touch (drag + pinch) ----------------------------------------

    def event(self, ev):
        t = ev.type()
        if t == QEvent.TouchBegin:
            ev.accept()
            pts = ev.touchPoints()
            if len(pts) == 1:
                self._drag_start = pts[0].pos().toPoint()
            elif len(pts) >= 2:
                self._pinch_dist = self._spread(pts)
            return True
        if t == QEvent.TouchUpdate:
            pts = ev.touchPoints()
            if len(pts) == 1 and self._drag_start is not None:
                self._drag_off = QPointF(pts[0].pos().toPoint() - self._drag_start)
                self.update()
            elif len(pts) >= 2:
                nd = self._spread(pts)
                if self._pinch_dist > 0 and nd > 0:
                    r = nd / self._pinch_dist
                    if r > 1.35:
                        self._zoom = min(18, self._zoom + 1)
                        self._pinch_dist = nd
                        self.update()
                    elif r < 0.7:
                        self._zoom = max(2, self._zoom - 1)
                        self._pinch_dist = nd
                        self.update()
            return True
        if t == QEvent.TouchEnd:
            pts = ev.touchPoints()
            if self._drag_start is not None:
                p0 = pts[0].pos() if pts else None
                if p0 is not None:
                    dx = p0.x() - self._drag_start.x()
                    dy = p0.y() - self._drag_start.y()
                    self._drag_start = None
                    self._drag_off = QPointF(0, 0)
                    if abs(dx) > 4 or abs(dy) > 4:
                        self._pan_px(-dx, -dy)
                    elif self._hit_recenter(p0.x(), p0.y()):
                        self._recenter()
                    else:
                        self.update()
                else:
                    self._drag_start = None
                    self._drag_off = QPointF(0, 0)
                    self.update()
            self._pinch_dist = 0.0
            return True
        return super().event(ev)

    @staticmethod
    def _spread(pts):
        if len(pts) < 2:
            return 0.0
        a, b = pts[0].pos(), pts[1].pos()
        return math.hypot(a.x() - b.x(), a.y() - b.y())

    # ---- geo helpers -------------------------------------------------

    def _recenter(self):
        self._lat = self._home_lat
        self._lng = self._home_lng
        self._zoom = 13
        self._panned = False
        self.update()

    def set_home(self, lat, lng):
        """Update home position (call from GPS provider when available)."""
        self._home_lat = lat
        self._home_lng = lng

    def _pan_px(self, dx, dy):
        z = self._zoom
        cx = _lng_to_tx(self._lng, z) + dx / TILE_PX
        cy = _lat_to_ty(self._lat, z) + dy / TILE_PX
        self._lng = _tx_to_lng(cx, z)
        self._lat = _ty_to_lat(cy, z)
        self._lat = max(-85.05, min(85.05, self._lat))
        self._panned = True
        self.update()

    # ---- joystick ----------------------------------------------------

    def handle_input(self, action: InputAction):
        PAN = 0.35
        if action == InputAction.CW:
            self._zoom = min(18, self._zoom + 1)
        elif action == InputAction.CCW:
            self._zoom = max(2, self._zoom - 1)
        elif action == InputAction.UP:
            self._pan_px(0, -TILE_PX * PAN)
        elif action == InputAction.DOWN:
            self._pan_px(0, TILE_PX * PAN)
        elif action == InputAction.LEFT:
            self._pan_px(-TILE_PX * PAN, 0)
        elif action == InputAction.RIGHT:
            self._pan_px(TILE_PX * PAN, 0)
        elif action == InputAction.PRESS:
            self._layer = (self._layer + 1) % len(TILE_URLS)
        else:
            return False
        self.update()
        return True


def MapView():
    return _MapWidget()
