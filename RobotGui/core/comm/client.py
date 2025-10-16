from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.subscribe as subscribe
from PySide6.QtCore import Qt, Slot
from RobotGui.core.comm.base_client import BaseMQTTClient
import RobotGui.core.comm.sub.coords as coords
from PySide6.QtGui import QKeyEvent

class CoordinatesClient(BaseMQTTClient):

    def __init__(self, address='localhost', port=1883):
        super().__init__(address, port)
        self.client.on_connect = self._on_connect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print('Failed to connect . Retrying...')
        else:
            subscribe.callback(coords.callback, 'robot/coordinates')

    def setup(self, coords_slot):
        coords.slot = coords_slot
        self.connect()

class Movement(BaseMQTTClient):
    def __init__(self):
        super().__init__()
        self.connect()

    @Slot(QKeyEvent)
    def handle(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:  # type: ignore[attr-defined]
            self.publish("robot/motion", "1,0")
        elif event.key() == Qt.Key_Down:  # type: ignore[attr-defined]
            self.publish("robot/motion", "-1,0")
        elif event.key() == Qt.Key_Right:  # type: ignore[attr-defined]
            self.publish("robot/motion", "0,1")
        elif event.key() == Qt.Key_Left:  # type: ignore[attr-defined]
            self.publish("robot/motion", "0,-1")

