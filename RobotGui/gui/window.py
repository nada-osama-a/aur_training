#from PySide6.QtGui import QKeyEvent
#from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout
#from RobotGui.gui.camera_display import CameraDisplay
#from RobotGui.gui.coordinates_display import CoordinatesDisplay
#
#from RobotGui.core.comm.client import setup
#
#class Window(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.setMinimumSize(640, 480)
#
#        self.setCentralWidget(CentralWidget())
#
#        self.show()
#
#    def keyPressEvent(self, event: QKeyEvent) -> None:
#        
#        return super().keyPressEvent(event)
#
#    
#
#class CentralWidget(QWidget):
#    def __init__(self, parent: QWidget | None = None):
#        super().__init__(parent)
#
#        self._layout = QVBoxLayout(self)
#        self._camera_widget = CameraDisplay()
#        self._layout.addWidget(self._camera_widget)
#
#        self._coordinates_widget = CoordinatesDisplay()
#        setup(self._coordinates_widget.update_coordinates)
#        self._layout.addWidget(self._coordinates_widget)
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from RobotGui.gui.camera_display import CameraDisplay
from RobotGui.gui.coordinates_display import CoordinatesDisplay


from RobotGui.core.comm.client import CoordinatesClient

from RobotGui.core.comm.pub.movement import Movement


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 480)
        self.setWindowTitle("Robot Control Interface")

        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        self.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        Movement.handle(event) 
        super().keyPressEvent(event)


class CentralWidget(QWidget):
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._layout = QVBoxLayout(self)

        self._camera_widget = CameraDisplay()
        self._layout.addWidget(self._camera_widget)

        self._coordinates_widget = CoordinatesDisplay()
        self._layout.addWidget(self._coordinates_widget)

        
        self._mqtt_client = CoordinatesClient()
        self._mqtt_client.setup(self._coordinates_widget.update_coordinates)
