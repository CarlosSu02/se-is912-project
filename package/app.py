from enum import Enum
import sys
import os
import typing
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QCloseEvent, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from package.helpers.tts import tts
from package.ui.custom_button import CustomQPButton
from package.ui.styles import get_stylesheet
from package.ui.toast_manager import toasts
from package.ui.windows.config_window import ConfigWindow
from package.utils.files import encode_to_base64, settings


# from package.helpers.screenshot import take_ss
from .helpers.screenshot import take_ss
from random import randint

VALUE_WH = 40
WINDOW_SIZE_WH = 60  # w = 60, h = 60, equal...

basic_qss = f"""
                QPushButton {{ 
                    color: #FFF;
                    background-color: #858580;
                    border-radius: 20px;
                    width: { VALUE_WH };
                    height: { VALUE_WH };
                }}
                QPushButton:hover {{
                    background-color: #757575;
                }}
            """

BG_TRANSPARENT = "background-color: rgba(0, 0, 0, 0.5)"


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, parent, window_key):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)
        # self.ui.closeButton.clicked.connect(text)
        self.parent = parent
        self.window_key = window_key

    def text(self):
        print("press!")

    def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
        print("close!")
        # self.close()

        if not hasattr(self.parent, "windows") or not isinstance(self.parent, QWidget):
            return

        self.parent.handle_windows(self.window_key)

        return super().closeEvent(a0)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent: QWidget | None = None):
        super().__init__(icon, parent)

        menu = QMenu(parent)
        exitAction = QAction(parent=menu, text="Exit")
        exitAction.triggered.connect(self.exit)

        menu.addAction(exitAction)
        self.setContextMenu(menu)

        self.activated.connect(
            # lambda reason: print(reason == QSystemTrayIcon.ActivationReason.Trigger)
            self.handle_window
        )

    def exit(self):
        print("exit!")
        # self.exit()
        QApplication.quit()

    # parent
    def handle_window(self, reason):
        widget = self.parent()
        if reason != QSystemTrayIcon.ActivationReason.Trigger or not isinstance(
            widget, QWidget
        ):
            return

        if not widget.isHidden():
            return widget.close()

        widget.show()
        widget.raise_()


# Para listar las ventanas disponibles
class Window(Enum):
    CONFIG = "config"
    OTHER = "other"


class MainWindow(QWidget):
    __windows_list = {Window.CONFIG: ConfigWindow, Window.OTHER: AnotherWindow}

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.setGeometry(0, 30, 100, 100)
        self.resize(WINDOW_SIZE_WH, WINDOW_SIZE_WH)
        self.setWindowTitle("First window PyQt6")

        self.topRightOffset()

        # Windows flags
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )

        # Window opacity
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.bgwidget = QWidget(self)
        # self.bgwidget.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.bgwidget.setObjectName("main-layout")

        self.bgwidget.setFixedWidth(60)
        self.bgwidget.setFixedHeight(60)

        self.main_layout = QVBoxLayout(self.bgwidget)

        self.init_content()

        # open_file(
        #     "./package/styles/styles.qss",
        #     mode="w",
        #     content="""QPushButton {color: white; }""",
        # )
        self.setStyleSheet(get_stylesheet())

        self.windows = {}
        self.show()

    def topRightOffset(self):
        fg = self.frameGeometry()
        screen = self.screen()

        if screen is None:
            return

        available_geometry = screen.availableGeometry()

        # print(available_geometry.topRight())

        x = available_geometry.right() - fg.width() - 10
        y = available_geometry.top() + 50

        self.move(x, y)

    def init_content(self):
        button_show = QPushButton(self)

        button_show.setCursor(Qt.CursorShape.PointingHandCursor)

        button_show.clicked.connect(self.handle_sec_layout)
        button_show.setProperty("class", "widget")
        button_show.setFixedSize(40, 40)

        self.main_layout.addWidget(button_show)

        # Secondary layout
        self.sec_layout = QVBoxLayout()
        self.sec_layout.setSpacing(10)  # Espaciado entre widgets
        self.sec_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Márgenes entre widgets y layout

        self.main_layout.addLayout(self.sec_layout)

    def functions(self):
        # button ss
        ss = CustomQPButton(icon="./icons/screenshot.svg", on_click=take_ss)

        # button_tts
        button_tts = CustomQPButton(text="🔈", on_click=tts)

        # button_close
        button_close = CustomQPButton(
            icon="./icons/close.svg", on_click=self.close_window
        )
        button_close.setProperty("class", "close")

        # button_file_imgs
        button_file_imgs = CustomQPButton(text="img", on_click=self.load_from_file)

        # button_config
        button_config = CustomQPButton(
            text="c",
            cursor=Qt.CursorShape.PointingHandCursor,
            on_click=lambda: self.handle_windows(Window.CONFIG),
        )

        # button_other
        button_other = CustomQPButton(
            text="o",
            cursor=Qt.CursorShape.PointingHandCursor,
            on_click=lambda: self.handle_windows(Window.OTHER),
        )

        ## Add to Secondary layout
        self.sec_layout.addWidget(ss)
        self.sec_layout.addWidget(button_tts)
        self.sec_layout.addWidget(button_file_imgs)
        self.sec_layout.addWidget(button_config)
        self.sec_layout.addWidget(button_other)
        self.sec_layout.addWidget(button_close)

        self.main_layout.addStretch()

        self.update_height()

    def handle_sec_layout(self):
        count = self.sec_layout.count()

        if count != 0:
            return self.clean_layout(self.sec_layout)

        return self.functions()

    # NOTE: with trayicon this closing does not work, it only minimizes the app.
    def close_window(self):
        self.handle_sec_layout()
        # self.close()
        QApplication.exit()

    def clean_layout(self, layout):  # : QVBoxLayout | None
        if layout is None:
            return

        for i in reversed(range(layout.count())):
            layout_item = layout.takeAt(i).widget()

            if layout_item:
                layout_item.deleteLater()

        self.update_height()

    def update_height(self):
        elements = self.sec_layout
        count = elements.count()

        spacing = elements.spacing()

        new_h = ((VALUE_WH + spacing) * count) + WINDOW_SIZE_WH

        self.setFixedHeight(new_h)
        self.bgwidget.setFixedHeight(new_h)

    def handle_windows(self, window_key):
        # print(self.__windows_list)
        # print(self.windows)

        window = window_key in self.windows

        if not window:
            # self.w = AnotherWindow(self)
            self.windows[window_key] = self.__windows_list[window_key](self, window_key)
            self.windows[window_key].show()

        else:
            # self.windows[window_key].close()
            del self.windows[window_key]

    def load_from_file(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Archivo", "", "Archivos de imagen (*.jpg *.png *.ico *.bmp)"
        )

        if not fileName:
            return

        try:
            file_name = os.path.basename(fileName)
            toasts().info(file_name)

            base64 = encode_to_base64(fileName)

            print(base64)

        except Exception as e:
            toasts().error(str(e))
            return

    # def closeEvent(self, event):
    #     event.ignore()  # Prevent the window from actually closing
    #     self.hide()  # Hide the window when the close button is pressed
    #     tray_icon.showMessage("App Hidden", "Click the tray icon to restore the app.")


# TODO: order code.
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(
    False
)  # Evita que la aplicación termine al cerrar la última ventana
window = MainWindow()

tray_icon = SystemTrayIcon(QIcon("./icons/ds.ico"), window)
tray_icon.show()
