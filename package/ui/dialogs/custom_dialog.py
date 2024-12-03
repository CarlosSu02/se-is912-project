from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QLabel,
    QDialog,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt

from package.ui.styles import get_stylesheet


class CustomDialog(QDialog):
    def __init__(self, content, fn_accept):
        if fn_accept is None:
            return

        super().__init__()

        self.setWindowTitle("Confirmación")
        self.setFixedSize(400, 120)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.setObjectName("custom-dialog")
        self.setStyleSheet(get_stylesheet())

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)

        # Button accepted
        self.buttonBox.accepted.connect(fn_accept)
        # self.buttonBox.setStyleSheet("background-color: red;")
        self.buttonBox.setStyleSheet("height: 30px;")
        self.buttonBox.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style the Ok button (accepted)
        ok_button = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok
        )  # Get the Ok button
        if ok_button is not None:
            ok_button.setProperty("class", "btn-danger not-rounded")
            ok_button.setText("Borrar")
            # ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        #     ok_button.setStyleSheet(
        #         "background-color: green; color: white; font-size: 16px; border-radius: 5px;"
        #     )

        # Style the Cancel button
        cancel_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel)
        if cancel_button is not None:
            cancel_button.setProperty("class", "qa-cancel not-rounded")
            cancel_button.setText("Cancelar")
            # cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        #     cancel_button.setStyleSheet(
        #         "background-color: red; color: white; font-size: 16px; border-radius: 5px;"
        #     )

        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(content)
        # message.setFont(QFont("Arial", 12))

        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
