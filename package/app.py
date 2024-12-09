import sys
import typing
from enum import Enum
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QCloseEvent, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMenu,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)
from package.helpers.functions import (
    handle_req_document,
    handle_req_files_media,
    handle_req_screeshot,
)
from package.ui.custom_button import CustomQPButton
from package.ui.styles import get_stylesheet
from package.ui.toast_manager import toasts
from package.ui.windows.config_window import ConfigWindow
from package.ui.windows.dotenv_window import Ui_DotEnvWindow
from package.ui.windows.graphics_window import Ui_GraphicsWindow
from package.ui.windows.question_window import QuestionWindow
from package.ui.windows.speech_window import Ui_SpeechWindow
from package.utils.handle_dotenv import exists_dotenv
from random import randint

VALUE_WH = 40
WINDOW_SIZE_WH = 60  # w = 60, h = 60, equal...

basic_qss = f"""
                QPushButton {{ 
                    color: #FFF;
                    background-color: #858580;
                    border-radius: 20px;
                    width: {VALUE_WH};
                    height: {VALUE_WH};
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
    QUESTION = "question"
    DOTENV = "dotenv"
    SPEECH = "speech"
    GRAPHICS = "graphics"


class MainWindow(QWidget):
    __windows_list = {
        Window.CONFIG: ConfigWindow,
        Window.OTHER: AnotherWindow,
        Window.QUESTION: QuestionWindow,
        Window.DOTENV: Ui_DotEnvWindow,
        Window.SPEECH: Ui_SpeechWindow,
        Window.GRAPHICS: Ui_GraphicsWindow,
    }

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
        self.bgwidget.setObjectName("bgwidget")

        self.main_layout = QVBoxLayout(self.bgwidget)

        self.init_content()
        self.functions()

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
        # button_show = QPushButton(self)

        # button_show.setCursor(Qt.CursorShape.PointingHandCursor)

        # button_show.clicked.connect(self.handle_sec_layout)

        button_show = CustomQPButton(
            icon="./icons/widget.svg", on_click=self.handle_sec_layout
        )

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
        self.buttons_widget = [
            ("./icons/screenshot.svg", "", self.handle_click_ss, True),
            ("./icons/file-image.svg", "", self.load_imgs_from_files, True),
            ("./icons/file-pdf.svg", "", self.load_docs_from_files, True),
            (
                "./icons/user-question-alt.svg",
                "",
                lambda: self.handle_windows(Window.QUESTION),
                True,
            ),
        ]

        for icon_path, style_class, fn, key_en in self.buttons_widget:
            button = CustomQPButton(icon=icon_path, on_click=fn)
            button.setProperty("class", style_class)
            button.setProperty("key_en", key_en)

            self.sec_layout.addWidget(button)

        button_update = CustomQPButton(
            text="up", on_click=lambda: self.setStyleSheet(get_stylesheet())
        )

        button_graphics = CustomQPButton(
            text="key",
            on_click=lambda: self.handle_windows(Window.GRAPHICS),
        )

        button_key = CustomQPButton(
            icon="./icons/key.svg",
            text="key",
            on_click=lambda: self.handle_windows(Window.DOTENV),
        )

        # button_close
        button_close = CustomQPButton(
            icon="./icons/close.svg", on_click=self.close_window
        )
        button_close.setProperty("class", "close")

        # Add to Secondary layout
        self.sec_layout.addWidget(button_graphics)
        self.sec_layout.addWidget(button_key)
        self.sec_layout.addWidget(button_close)
        self.sec_layout.addWidget(button_update)

        self.main_layout.addStretch()

        self.update_height()
        self.enabled_items()

    def handle_sec_layout(self):
        count = self.sec_layout.count()

        if count != 0:
            return self.clean_layout(self.sec_layout)

        return self.functions()

    def close_window(self):
        self.handle_sec_layout()
        # self.close()
        QApplication.exit()  # NOTE: <- temporally

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

    def handle_windows(self, window_key, *args, **kwargs):
        # print(self.__windows_list)
        # print(self.windows)

        exists_window = window_key in self.windows

        if not exists_window:
            # self.w = AnotherWindow(self)
            window = self.__windows_list[window_key]
            content = kwargs.get("content", None)
            self.windows[window_key] = (
                window(self, window_key)
                if content is None
                else window(self, window_key, content)
            )

            if content is None:
                self.windows[window_key].show()

        else:
            # self.windows[window_key].close()
            del self.windows[window_key]

    def enabled_items(self):
        if self.sec_layout is None:
            return

        enabled = exists_dotenv()

        for i in reversed(range(self.sec_layout.count())):
            layout_item = self.sec_layout.itemAt(i).widget()

            if layout_item:
                prop = layout_item.property("key_en")
                if prop:
                    layout_item.setEnabled(enabled)

    def load_imgs_from_files(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Archivo", "", "Archivos de imagen (*.jpg *.png *.ico *.bmp)"
        )

        text = handle_req_files_media(fileName)

        self.handle_speech(text)

    def load_docs_from_files(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Archivo", "", "Archivos de documentos (*.pdf)"
        )

        # handle_req_image(fileName)
        text = handle_req_document(fileName)

        self.handle_speech(text)

    def handle_click_ss(self):
        self.close()  # Close widget before take_ss

        text = handle_req_screeshot()

        self.show()  # Open widget after take_ss

        self.handle_speech(text)
        # self.handle_windows(Window.SPEECH)

    # handle_speech => para manejo del tts global, ya que todas las ventanas y funciones podrían tener acceso a este método
    # se le pasa el texto y nada más
    def handle_speech(self, text):
        try:
            if text is None:
                raise Exception("Ocurrió un error, por favor inténtelo más tarde.")

            # if Window.SPEECH in self.windows:
            #     self.handle_windows(Window.SPEECH)

            if Ui_SpeechWindow.check_existing_instance():
                return

            self.handle_windows(Window.SPEECH, content=text)

        except Exception as e:
            toasts().error(e)


# TODO: order code.
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(
    False
)  # Evita que la aplicación termine al cerrar la última ventana
window = MainWindow()

tray_icon = SystemTrayIcon(QIcon("./icons/widget.ico"), window)
tray_icon.show()