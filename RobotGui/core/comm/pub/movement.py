from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QKeyEvent
from RobotGui.core.comm.base_client import BaseMQTTClient

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
