from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Slot

class CoordinatesDisplay(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._label = QLabel(self)
        self._label.setText('Robot is not connected.')

    @Slot()
    def update_coordinates(self, x: float, y: float):
        self._label.setText(f'Robot is at: {x}, {y}')