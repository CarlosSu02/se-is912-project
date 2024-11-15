import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from package.helpers.tts import tts
from package.ui.styles import get_stylesheet


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


class AnotherWindow1(QWidget):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.setLayout(layout)


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, fn):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)
        # self.ui.closeButton.clicked.connect(text)
        self.fn = fn

    def text(self):
        print("press!")

    def closeEvent(self, event):
        print("close!")
        self.close()
        self.fn.w = None


class Window(QWidget):
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
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
            # | Qt.WindowType.Tool
        )

        # Window opacity
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.bgwidget = QWidget(self)
        # self.bgwidget.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

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

        self.w = None
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
        # button_show.setText("show")

        button_show.setCursor(Qt.CursorShape.PointingHandCursor)

        button_show.clicked.connect(self.handle_sec_layout)

        self.main_layout.addWidget(button_show)

        # Secondary layout
        self.sec_layout = QVBoxLayout()
        self.main_layout.addLayout(self.sec_layout)

    def functions(self):
        ss = QPushButton(self)

        ss.setCursor(Qt.CursorShape.PointingHandCursor)
        ss.setIcon(QIcon("./icons/screenshot.svg"))

        ss.clicked.connect(take_ss)

        button_new_window = QPushButton("+", self)

        button_new_window.setCursor(Qt.CursorShape.PointingHandCursor)
        button_new_window.clicked.connect(self.new_window)

        button_tts = QPushButton("🔈", self)

        button_tts.setCursor(Qt.CursorShape.PointingHandCursor)
        button_tts.clicked.connect(tts)

        button_close = QPushButton(self)

        button_close.setCursor(Qt.CursorShape.PointingHandCursor)
        button_close.setIcon(QIcon("./icons/close.svg"))
        button_close.setProperty("class", "close")

        button_close.clicked.connect(self.close)

        ## Add to Secondary layout
        self.sec_layout.addWidget(ss)
        self.sec_layout.addWidget(button_new_window)
        self.sec_layout.addWidget(button_tts)
        self.sec_layout.addWidget(button_close)

        self.main_layout.addStretch()

        self.update_height()

    def handle_sec_layout(self):
        # print(self.sec_layout.count())
        count = self.sec_layout.count()

        # self.clean_layout(self.sec_layout) if count != 0 else self.functions()
        if count != 0:
            return self.clean_layout(self.sec_layout)

        return self.functions()

    def close_window(self):
        self.close()

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

        # if count == 0:
        #     return

        # one = elements.itemAt(0).widget()

        # if one:
        #     print(one.widget().height())

        spacing = elements.spacing()

        new_h = ((VALUE_WH + spacing) * count) + WINDOW_SIZE_WH

        self.setFixedHeight(new_h)
        self.bgwidget.setFixedHeight(new_h)

    def new_window(self):
        if self.w is None:
            self.w = AnotherWindow(self)
            self.w.show()

        else:
            self.w.close()
            self.w = None


# TODO: search QSystemTrayIcon
app = QApplication(sys.argv)
window = Window()
