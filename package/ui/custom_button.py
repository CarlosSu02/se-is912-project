from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QPushButton


class CustomQPButton(QPushButton):
    def __init__(
        self,
        text="?",
        cursor=Qt.CursorShape.PointingHandCursor,
        icon: str | None = None,
        on_click=lambda: print("function"),
    ):
        super().__init__()
        self.setText(text) if icon is None else self.setIcon(QIcon(icon))
        self.setCursor(cursor)
        self.clicked.connect(on_click)
