import typing
from random import randint
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QFont, QPixmap
from PyQt6.QtWidgets import QComboBox, QLabel, QSizePolicy, QVBoxLayout, QWidget

from package.utils.files import HandleJson, config_path


class ConfigWindow(QWidget):
    def __init__(self, parent, window_key):
        super().__init__()
        # self.layout = QVBoxLayout()
        # # self.label = QLabel("Another Window? % d" % randint(0, 100))
        # self.label = QLabel("Prompts de expertos:")
        # self.layout.addWidget(self.label)
        # self.setLayout(self.layout)

        self.parent = parent
        self.window_key = window_key

        self.main_layout = QVBoxLayout(self)

        self.initUI()

    def initUI(self):
        # self.resize(250, 100)
        self.setFixedSize(250, 100)
        self.setWindowTitle("Configuración")

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.prompts()

    def prompts(self):
        prompts = HandleJson("./config/prompts.json")
        config = HandleJson(config_path)

        if prompts.data is None:
            return

        # dict_keys = type(dict[str, str]().keys())
        self.items_combobox: list[str] = list(prompts.data.keys())
        self.default_prompt = config.get_value("expert")

        # print(len(prompts.data.keys()))
        # print(list(prompts.data.keys()))
        # print(", ".join(prompts.data.keys()))

        # label = QLabel(", ".join(prompts.data.keys()))

        layout = QVBoxLayout()

        label = QLabel("Prompts de expertos:", self)
        label.setFont(QFont("Arial", 12))
        # label.move(20, 50)

        combobox = QComboBox()
        combobox.addItems(prompts.data.keys())
        combobox.setFont(QFont("Arial", 12))
        # combobox.setFixedSize(self.width(), 30)
        # combobox.resize(combobox.sizeHint())
        # combobox.move(90, 50)
        combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        combobox.setMinimumHeight(30)

        combobox.setCurrentIndex(self.items_combobox.index(self.default_prompt))

        combobox.setStyleSheet(
            """
            QComboBox {
                padding-left: 10px;  /* Space inside the combo box */
            }
        """
        )
        combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        view = combobox.view()
        if view:
            view.setCursor(Qt.CursorShape.PointingHandCursor)

        combobox.currentTextChanged.connect(self.handle_change_combobox)

        layout.addWidget(label)
        layout.addWidget(combobox)

        self.main_layout.addLayout(layout)

    def handle_change_combobox(self, value):
        if value == self.default_prompt:
            return

        print(f"combobox change: { value }")

    def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
        # return super().closeEvent(a0)

        print("close config window")
        # self.parent.handle_windows()
        # self.parent.handle_windows()
        if not hasattr(self.parent, "windows") or not isinstance(self.parent, QWidget):
            return

        # del self.parent.windows[self.window_key]
        self.parent.handle_windows(self.window_key)
        # self.close()

        # a0.accept()
        return super().closeEvent(a0)
