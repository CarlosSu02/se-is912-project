# Form implementation generated from reading ui file 'designer/speech_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import math
import os.path
from posixpath import expanduser
import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QFileDialog

from package.ui.components import CustomQPButton
from package.ui.dialogs.toast_manager import toasts
from package.utils import TTSThread, text_to_file_audio, text_to_docx, markdown_to_text, convert_md_to_docx


class Ui_SpeechWindow(QWidget):
    _tts_active = False
    _active_instance = None

    def __init__(self, parent, window_key, text):
        super().__init__()

        if Ui_SpeechWindow._tts_active:
            print("se encuentra activo")
            return

        Ui_SpeechWindow._tts_active = True
        Ui_SpeechWindow._active_instance = self

        self.parent = parent
        self.window_key = window_key
        self.text = text
        self.tts_thread = None

        self.setupUi()
        self.show()
        self.init_tts()

    def setupUi(self):
        self.setObjectName("SpeechWindow")

        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("horizontal_layout")

        self.main_vertical_layout = QtWidgets.QVBoxLayout()
        self.main_vertical_layout.setObjectName("main_vertical_layout")

        self.textarea()
        self.buttons()

        self.setFixedSize(365, 556) if hasattr(self, "response_textarea") else self.setFixedSize(190, 95)

        self.horizontal_layout.addLayout(self.main_vertical_layout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # self.topRightOffset(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SpeechWindow", "Respuesta"))
        self.label_stop.setText(_translate("SpeechWindow", "Parar"))
        self.label_download.setText(_translate("SpeechWindow", "Descargar"))

    def textarea(self):
        self.response_textarea = QtWidgets.QPlainTextEdit(self)
        # self.response_textarea.setEnabled(False)
        self.response_textarea.setReadOnly(True)
        self.response_textarea.setObjectName("response_textarea")
        self.response_textarea.setPlainText(self.text)

        self.main_vertical_layout.addWidget(self.response_textarea)

    def buttons(self):
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")

        spacer_start = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(spacer_start)
        # Layout stop
        self.layout_stop = QtWidgets.QVBoxLayout()
        self.layout_stop.setObjectName("layout_stop")

        # Button stop
        # self.button_stop = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.button_stop = CustomQPButton(on_click=self.tts_stop)
        self.button_stop.setMinimumSize(QtCore.QSize(0, 48))
        self.button_stop.setStyleSheet("border:none; background-color: transparent;")
        self.button_stop.setText("")

        icon_stop = QtGui.QIcon()
        icon_stop.addPixmap(
            QtGui.QPixmap("./icons/stop.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.button_stop.setIcon(icon_stop)

        self.button_stop.setIconSize(QtCore.QSize(32, 32))
        self.button_stop.setObjectName("button_stop")

        self.layout_stop.addWidget(self.button_stop)

        # Label stop
        self.label_stop = QtWidgets.QLabel(self)
        self.label_stop.setObjectName("label_stop")
        # self.label_stop.setStyleSheet("align-text: center;")
        self.label_stop.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout_stop.addWidget(self.label_stop)

        self.buttons_layout.addLayout(self.layout_stop)
        spacer_middle = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.buttons_layout.addItem(spacer_middle)

        # Layout download
        self.layout_download = QtWidgets.QVBoxLayout()
        self.layout_download.setObjectName("layout_download")

        # Button download
        # self.button_download = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.button_download = CustomQPButton(on_click=self.save_files)
        self.button_download.setMinimumSize(QtCore.QSize(0, 48))
        self.button_download.setStyleSheet(
            "border:none; background-color: transparent;"
        )
        self.button_download.setText("")

        icon_download = QtGui.QIcon()
        icon_download.addPixmap(
            QtGui.QPixmap("./icons/download.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.button_download.setIcon(icon_download)

        self.button_download.setIconSize(QtCore.QSize(24, 24))
        self.button_download.setObjectName("button_download")

        self.layout_download.addWidget(self.button_download)

        # Label download
        self.label_download = QtWidgets.QLabel(self)
        self.label_download.setObjectName("label_download")
        self.label_download.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout_download.addWidget(self.label_download)
        self.buttons_layout.addLayout(self.layout_download)

        spacer_end = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.buttons_layout.addItem(spacer_end)

        self.main_vertical_layout.addLayout(self.buttons_layout)

    def topRightOffset(self, obj):
        fg = obj.frameGeometry()
        screen = obj.screen()

        if screen is None:
            return

        available_geometry = screen.availableGeometry()

        x = math.floor((available_geometry.right() - fg.width()) / 2)
        # x = math.floor((available_geometry.right()) / 2) - fg.width()

        y = available_geometry.top()

        fg.moveCenter(available_geometry.center())

        obj.move(x, y)

    def init_tts(self):
        if self.tts_thread is not None and self.tts_thread.isRunning():
            print("El TTS ya está en ejecución.")
            return

        self.tts_thread = TTSThread(markdown_to_text(self.text))
        self.tts_thread.finished.connect(self.on_tts_finished)
        self.tts_thread.error.connect(self.on_tts_error)

        # self.tts_thread.stop()  # En dado caso se encuentre en el loop
        self.tts_thread.start()

    def tts_stop(self):
        if self.tts_thread is None:
            return

        if self.tts_thread.isRunning():
            self.tts_thread.stop()
            self.tts_thread.quit()

    @pyqtSlot()
    def on_tts_finished(self):
        print("TTS finished!")

        self.tts_thread = None

        Ui_SpeechWindow._tts_active = False
        Ui_SpeechWindow._active_instance

    @pyqtSlot(str)
    def on_tts_error(self, error):
        toasts().error(error)

        Ui_SpeechWindow._tts_active = False
        Ui_SpeechWindow._active_instance = None

    @staticmethod
    def check_existing_instance():
        if Ui_SpeechWindow._tts_active and Ui_SpeechWindow._active_instance:
            instance = Ui_SpeechWindow._active_instance
            instance.raise_()  # Lleva la ventana existente al frente
            toasts().info("La ventana de TTS ya está abierta.")
            return True
        return False

    def get_dir(self):
        # fileName
        # dir = QFileDialog.getExistingDirectory(
        #     parent=self,
        #     caption=str("Open Directory"),
        #     directory=expanduser("~"),
        #     options=QFileDialog.Option.ShowDirsOnly
        #     | QFileDialog.Option.DontResolveSymlinks,
        # )

        dir, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Guardar Archivo",
            directory=expanduser("~"),
            filter="Documento de Word (*.docx)",
        )

        if not dir:
            return

        return dir

    def save_files(self):
        try:
            if self.tts_thread:
                self.tts_thread.stop()

            dir = self.get_dir()

            if dir is None:
                raise Exception("No se seleccionó un directorio.")

            file_name = list(os.path.basename(dir).split("."))
            file_name.pop()
            file_name = f"{os.path.dirname(dir)}/{".".join(file_name)}"

            docx = f"{file_name}.docx"
            mp4 = f"{file_name}.mp4"

            # text_to_docx(self.text, docx)
            text_to_file_audio(self.text, mp4)
            convert_md_to_docx(self.text, docx)

            self.close()

            toasts().success(f"Se guardaron los archivos en {os.path.dirname(dir)}.")

        except Exception as e:
            toasts().error(e)

    def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
        self.tts_stop()

        if not hasattr(self.parent, "windows") or not isinstance(self.parent, QWidget):
            return

        self.parent.handle_windows(self.window_key)

        Ui_SpeechWindow._tts_active = False
        Ui_SpeechWindow._active_instance = None

        return super().closeEvent(a0)