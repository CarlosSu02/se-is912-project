from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from package.core.enums import Icon, Cursor


class CustomQPButton(QPushButton):
    def __init__(
            self,
            text="?",
            cursor: Cursor = Cursor.POINTING,
            icon: Icon | None = None,
            on_click=lambda: print("function"),
    ):
        super().__init__()
        self.setText(text) if icon is None else self.setIcon(QIcon(f"./icons/{icon.value}"))
        self.setCursor(cursor.value)
        self.clicked.connect(on_click)