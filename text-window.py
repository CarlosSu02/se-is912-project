import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.setFixedSize(200, 200)
        self.show()


app = QApplication(sys.argv)
window = TestWindow()
sys.exit(app.exec())
