from types import MethodType
from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt


class CustomDialog(QDialog):
    def __init__(self, content, fn_accept):
        if fn_accept is None:
            return

        super().__init__()

        self.setWindowTitle("Confirmación")
        self.resize(300, 100)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)

        # Button accepted
        self.buttonBox.accepted.connect(fn_accept)
        self.buttonBox.setStyleSheet("background-color: red;")

        # Style the Ok button (accepted)
        ok_button = self.buttonBox.button(QDialogButtonBox.Ok)  # Get the Ok button
        if ok_button is not None:
            ok_button.setStyleSheet(
                "background-color: green; color: white; font-size: 16px; border-radius: 5px;"
            )

        # Style the Cancel button
        cancel_button = self.buttonBox.button(QDialogButtonBox.Cancel)
        if cancel_button is not None:
            cancel_button.setStyleSheet(
                "background-color: red; color: white; font-size: 16px; border-radius: 5px;"
            )

        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(content)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
