from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, QSizePolicy
from RobotGui.gui.camera_display import CameraDisplay
from RobotGui.gui.coordinates_display import CoordinatesDisplay

from RobotGui.core.comm.client import CoordinatesClient, Movement


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 480)
        self.setWindowTitle("Robot Control Interface")

        self._mqtt_client = CoordinatesClient()

        self.central_widget = CentralWidget(self._mqtt_client)
        self.setCentralWidget(self.central_widget)
        self.show()

        self._movement_client = Movement()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self._movement_client.handle(event)
        super().keyPressEvent(event)


class CentralWidget(QWidget):
    def __init__(self, mqtt_client: CoordinatesClient, parent: QWidget | None = None):
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self._camera_widget = CameraDisplay()
        self._camera_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)    
        self._layout.addWidget(self._camera_widget)

        self._coordinates_widget = CoordinatesDisplay()
        self._coordinates_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = self._coordinates_widget.font()  
        font.setPointSize(18)  
        self._coordinates_widget.setFont(font)

        self._layout.addWidget(self._coordinates_widget)

        mqtt_client.setup(self._coordinates_widget.update_coordinates)


