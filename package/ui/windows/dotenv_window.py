# Form implementation generated from reading ui file 'designer/dotenv_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from dotenv import load_dotenv
from pyqttoast import toast
from package.ui.dialogs.custom_dialog import CustomDialog
from package.ui.toast_manager import toasts
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QDialog,
)
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtCore import Qt, pyqtBoundSignal


from package.ui.custom_button import CustomQPButton
from package.ui.styles import get_stylesheet
from package.utils.handle_dotenv import (
    delete_key,
    exists_dotenv,
    clients,
    get_env,
    key_from_value,
    set_env,
    validate_key,
)


class Ui_DotEnvWindow(QWidget):
    def __init__(self, parent, window_key):
        super().__init__()

        self.parent = parent
        self.window_key = window_key

        self.setStyleSheet(get_stylesheet())
        self.setupUi(self)

    def dotenv(self):
        return exists_dotenv()

    def setupUi(self, DotEnvWindow):
        DotEnvWindow.setObjectName("DotEnvWindow")
        DotEnvWindow.resize(500, 774)

        DotEnvWindow.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # self.retranslateUi(DotEnvWindow)
        # self.set_key(self)

        exists_env = self.dotenv()

        # self.update_height()
        print(exists_env)

        self.set_key(self) if not exists_env else self.get_key(self)

        QtCore.QMetaObject.connectSlotsByName(DotEnvWindow)

    # def retranslateUi(self, DotEnvWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     DotEnvWindow.setWindowTitle(_translate("DotEnvWindow", "Key"))
    #     self.label_platform.setText(_translate("DotEnvWindow", "Plataforma"))
    #     self.label.setText(_translate("DotEnvWindow", "Ingrese la clave"))
    #     self.button_add.setText(_translate("DotEnvWindow", "Agregar"))
    #     self.button_add.setProperty(
    #         "class", _translate("DotEnvWindow", "qa-save not-rounded")
    #     )
    #     self.button_cancel.setText(_translate("DotEnvWindow", "Cancelar"))
    #     self.button_cancel.setProperty(
    #         "class", _translate("DotEnvWindow", "qa-cancel not-rounded")
    #     )
    #     self.button_close.setText(_translate("DotEnvWindow", "Cerrar"))
    #     self.button_close.setProperty(
    #         "class", _translate("DotEnvWindow", "qa-cancel not-rounded")
    #     )
    #     self.label_platform_2.setText(_translate("DotEnvWindow", "Plataforma"))
    #     self.label_2.setText(
    #         _translate("DotEnvWindow", "API KEY DE UNA PLATAFORMA??????")
    #     )

    """
    def get_key(self, DotEnvWindow):
        self.sec_widget = QWidget(parent=DotEnvWindow)
        self.sec_widget.setEnabled(True)
        self.sec_widget.setGeometry(QtCore.QRect(20, 20, 461, 141))
        # self.sec_widget.resize(461, 141)
        self.sec_widget.setObjectName("sec_widget")

        # self.layoutWidget = QWidget(parent=self.sec_widget)
        # self.layoutWidget.setGeometry(QtCore.QRect(0, 100, 461, 30))
        # self.layoutWidget.setObjectName("layoutWidget")

        self.sec_layout = QVBoxLayout(self.sec_widget)
        self.sec_layout.setContentsMargins(0, 0, 0, 0)
        self.sec_layout.setObjectName("sec_layout")

        # self.horizontalLayout_2 = QHBoxLayout(self.sec_widget)
        # self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # spacerItem1 = QSpacerItem(
        #     40,
        #     20,
        #     QSizePolicy.Policy.Expanding,
        #     QSizePolicy.Policy.Minimum,
        # )
        #
        # self.horizontalLayout_2.addItem(spacerItem1)

        # Title
        self.label_platform_key = QLabel("Plataforma", parent=self.sec_widget)
        self.label_platform_key.setGeometry(QtCore.QRect(0, 0, 459, 30))
        self.label_platform_key.setMinimumSize(QtCore.QSize(0, 30))
        # self.label_platform_key.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_platform_key.setObjectName("label_platform_key")

        # Widget para el label de key
        self.key_widget = QWidget(parent=self.sec_widget)
        self.key_widget.setGeometry(QtCore.QRect(0, 30, 461, 63))
        # self.key_widget.setStyleSheet("border: 1px solid red;")
        self.key_widget.setObjectName("key_widget")

        self.horizontalLayout_3 = QHBoxLayout(self.key_widget)
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label_key = QLabel("API Key", parent=self.key_widget)
        self.label_key.setObjectName("label_key")

        self.horizontalLayout_3.addWidget(self.label_key)

        spacerItem2 = QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.horizontalLayout_3.addItem(spacerItem2)

        self.button_delete_key = QPushButton(parent=self.key_widget)
        self.button_delete_key.setEnabled(True)
        self.button_delete_key.setMinimumSize(QtCore.QSize(40, 40))
        # self.button_delete_key.setMaximumSize(QtCore.QSize(16777215, 16777200))
        self.button_delete_key.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )

        self.button_delete_key.setStyleSheet("height: 32px;")
        self.button_delete_key.setText("")

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("designer/C:/Users/carlossup/.designer/icons/screenshot.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )

        self.button_delete_key.setIcon(icon)
        self.button_delete_key.setObjectName("button_delete_key")

        self.horizontalLayout_3.addWidget(self.button_delete_key)

        # self.button_close = QPushButton(parent=self.sec_widget)
        # self.button_close.setObjectName("button_close")

        # Botón Close debajo del key_widget
        self.button_close = QPushButton("Close", parent=self.sec_widget)
        self.button_close.setMinimumSize(QtCore.QSize(0, 40))
        self.button_close.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.button_close.setObjectName("button_close")

        self.sec_layout.addWidget(
            self.button_close
        )  # self.sec_layout.addWidget(self.button_close)

        self.sec_widget.setFixedHeight(self.sec_widget.height())

        self.update_height(self.sec_widget)
    """

    def get_key(self, DotEnvWindow):
        self.sec_widget = QWidget(parent=DotEnvWindow)
        self.sec_widget.setEnabled(True)
        self.sec_widget.setGeometry(QtCore.QRect(20, 20, 461, 141))
        self.sec_widget.setObjectName("sec_widget")

        self.sec_layout = QVBoxLayout(self.sec_widget)
        self.sec_layout.setContentsMargins(0, 0, 0, 0)
        self.sec_layout.setObjectName("sec_layout")

        # Etiqueta superior
        self.label_platform_key = QLabel("Plataforma", parent=self.sec_widget)
        self.label_platform_key.setMinimumSize(QtCore.QSize(0, 30))
        self.label_platform_key.setObjectName("label_platform_key")
        self.sec_layout.addWidget(self.label_platform_key)

        # Widget para la clave
        self.key_widget = QWidget(parent=self.sec_widget)
        self.key_widget.setObjectName("key_widget")

        self.horizontalLayout_3 = QHBoxLayout(self.key_widget)
        # self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_3.setContentsMargins(
            10, 5, 10, 5
        )  # left, top, right, bottom
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Title current api key
        current_api_key = key_from_value(get_env())
        self.label_key = QLabel(current_api_key, parent=self.key_widget)
        self.label_key.setObjectName("label_key")

        self.horizontalLayout_3.addWidget(self.label_key)

        spacerItem2 = QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_3.addItem(spacerItem2)

        self.button_delete_key = QPushButton(parent=self.key_widget)
        self.button_delete_key.setEnabled(True)
        self.button_delete_key.setMinimumSize(QtCore.QSize(40, 40))
        self.button_delete_key.setCursor(
            QtGui.QCursor(Qt.CursorShape.PointingHandCursor)
        )
        # self.button_delete_key.setStyleSheet("height: 32px;")
        self.button_delete_key.setText("")
        self.button_delete_key.clicked.connect(self.handle_delete_env)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("./icons/trash.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.button_delete_key.setIcon(icon)
        self.button_delete_key.setObjectName("button_delete_key")
        self.button_delete_key.setProperty("class", "btn-danger")

        self.horizontalLayout_3.addWidget(self.button_delete_key)

        self.sec_layout.addWidget(self.key_widget)

        # Botón Close debajo del key_widget
        # self.button_close = QPushButton("Close", parent=self.sec_widget)
        # self.button_close.setMinimumSize(QtCore.QSize(0, 40))
        # self.button_close.setCursor(
        #     QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        # )
        # self.button_close.setObjectName("button_close")

        # Crear un layout horizontal para posicionar el botón "close"
        self.close_button_layout = QHBoxLayout()
        self.close_button_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        self.close_button_layout.setSpacing(0)

        # Añadir un espaciador a la izquierda para empujar el botón hacia la derecha
        spacer_left = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.close_button_layout.addItem(spacer_left)

        # Crear el botón "close"
        self.button_close = QPushButton("Cerrar", parent=self.sec_widget)
        self.button_close.setMinimumSize(QtCore.QSize(80, 40))  # Tamaño mínimo
        self.button_close.clicked.connect(self.close)
        self.button_close.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.close_button_layout.addWidget(self.button_close)

        # Añadir el layout horizontal (con el botón alineado a la derecha) al layout vertical principal
        self.sec_layout.addLayout(self.close_button_layout)
        # self.sec_layout.addWidget(self.button_close)

        self.sec_widget.setFixedHeight(self.sec_widget.height())
        self.update_height(self.sec_widget)

    # Agregar key
    def set_key(self, DotEnvWindow):
        self.verticalLayoutWidget = QWidget(parent=DotEnvWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 19, 461, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.main_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")

        self.label_platform = QLabel("Plataforma", parent=self.verticalLayoutWidget)
        self.label_platform.setMinimumSize(QtCore.QSize(0, 30))
        # self.label_platform.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_platform.setObjectName("label_platform")

        self.main_layout.addWidget(self.label_platform)

        self.combobox = QComboBox(parent=self.verticalLayoutWidget)
        self.combobox.setObjectName("combobox")

        ## add items
        items_combobox = list(clients.keys())
        self.combobox.addItems(items_combobox)

        self.combobox.setStyleSheet(
            """
            QComboBox {
                padding-left: 10px;  /* Space inside the combo box */
            }
            """
        )
        self.combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        view = self.combobox.view()
        if view:
            view.setCursor(Qt.CursorShape.PointingHandCursor)

        self.main_layout.addWidget(self.combobox)

        self.label_key_textarea = QLabel(
            "Ingrese la clave", parent=self.verticalLayoutWidget
        )
        self.label_key_textarea.setMinimumSize(QtCore.QSize(0, 30))
        # self.label_key_textarea.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_key_textarea.setObjectName("label_key_textarea")

        self.main_layout.addWidget(self.label_key_textarea)

        self.key_textarea = QPlainTextEdit(parent=self.verticalLayoutWidget)
        self.key_textarea.setPlaceholderText("API Key")
        self.key_textarea.setMinimumSize(QtCore.QSize(0, 100))
        self.key_textarea.setMaximumSize(QtCore.QSize(16777215, 100))
        self.key_textarea.setObjectName("key_textarea")

        self.key_textarea.textChanged.connect(self.handle_text_changed)

        self.main_layout.addWidget(self.key_textarea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 20, 0, 0)

        spacerItem = QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.horizontalLayout.addItem(spacerItem)

        # self.button_add = QPushButton("Agregar", parent=self.verticalLayoutWidget)
        # self.button_add.setObjectName("button_add")

        self.button_add = CustomQPButton("Agregar", on_click=self.handle_add_env)
        self.button_add.setProperty("class", "qa-save not-rounded")
        self.button_add.setEnabled(False)

        self.horizontalLayout.addWidget(self.button_add)

        # self.button_cancel = QPushButton("Cancelar", parent=self.verticalLayoutWidget)
        # self.button_cancel.setObjectName("button_cancel")
        # self.button_cancel.clicked.connect(self.close)

        self.button_cancel = CustomQPButton(text="Cancelar", on_click=self.close)
        self.button_cancel.setProperty("class", "qa-cancel not-rounded")

        self.horizontalLayout.addWidget(self.button_cancel)

        self.main_layout.addLayout(self.horizontalLayout)
        # self.main_layout.setStretch(0, 1)
        # self.main_layout.setStretch(1, 1)
        # self.main_layout.setStretch(3, 1)
        # self.main_layout.setStretch(4, 1)

        self.update_height(self.verticalLayoutWidget)

        return

    def update_height(self, widget):
        print(widget.height())
        self.setFixedWidth(widget.width() + 40)
        self.setFixedHeight(widget.height() + 30)

        return

    def handle_text_changed(self):
        value = self.key_textarea.toPlainText().strip()

        # condition = len(value) < 10

        # if len(value) < 10:
        #     return

        condition = bool(validate_key(value))

        self.button_add.setEnabled(condition)

    def handle_add_env(self):
        key = clients[self.combobox.currentText().strip()]
        value = self.key_textarea.toPlainText().strip()

        save = set_env(key, value)

        if save is None:
            return toasts().error("Ocurrió un error al guardar la key.")

        # The error is handling in open_file function on set_env
        toasts().success("Se agregó la API Key al archivo .env.")

        self.close()

    def handle_delete_env(self):
        key = self.label_key.text()  # solo para obtener el titulo de la actual key
        self.close()

        self.dlg = CustomDialog(
            content=f"Desea eliminar la API Key de { key }?",
            fn_accept=lambda: self.handle_delete_env_conf(key),
        )
        if self.dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

        # dlg = QDialog(self)
        # dlg.setWindowTitle("HELLO!")
        # dlg.exec()

    def handle_delete_env_conf(self, key):
        # print(key)
        delete = delete_key(key)

        self.dlg.close()

        if not delete:
            return toasts().error("Ocurrió un error al eliminar la API Key.")

        return toasts().success("¡La API Key se eliminó con éxito!")

    def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
        if not hasattr(self.parent, "windows") or not isinstance(self.parent, QWidget):
            return

        self.parent.handle_windows(self.window_key)

        return super().closeEvent(a0)
