import typing
from random import randint
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QFont, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from package.ui.custom_button import CustomQPButton
from package.ui.styles import get_stylesheet
from package.ui.toast_manager import toasts
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

        self.setStyleSheet(get_stylesheet())

        self.initUI()

    def initUI(self):
        # self.resize(250, 100)
        self.setFixedSize(350, 140)
        self.setWindowTitle("Configuración")
        QApplication.setFont(QFont("Arial", 10))

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.prompts()
        self.buttons()
        self.update_height()

    def prompts(self):
        prompts = HandleJson("./config/prompts.json")
        self.config = HandleJson(config_path)

        if prompts.data is None:
            return

        # dict_keys = type(dict[str, str]().keys())
        self.items_combobox: list[str] = list(prompts.data.keys())
        self.default_prompt = self.config.get_value("expert")

        # print(len(prompts.data.keys()))
        # print(list(prompts.data.keys()))
        # print(", ".join(prompts.data.keys()))

        # label = QLabel(", ".join(prompts.data.keys()))

        self.container_prompts = QWidget()
        container_layout = QVBoxLayout(self.container_prompts)

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
        combobox.setFixedHeight(30)

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

        container_layout.addWidget(label)
        container_layout.addWidget(combobox)
        self.container_prompts.setFixedHeight(label.height() + combobox.height())

        # self.main_layout.addLayout(container_layout)
        self.main_layout.addWidget(self.container_prompts)
        self.main_layout.addStretch(0)

    def buttons(self):
        self.container_buttons = QWidget()
        container_buttons_layout = QHBoxLayout(self.container_buttons)

        container_buttons_layout.addStretch()

        buttons = [
            ("Guardar", "save", self.handle_click_save),
            ("Cancelar", "close", self.close),
        ]
        button_height = 30

        for name, style_class, fn in buttons:
            print(name, style_class)
            button = CustomQPButton(text=name, on_click=fn)
            # button.setObjectName("not-rounded")
            # button.setProperty("class", "not-rounded")
            # button.setProperty("class", style_class)
            button.setProperty("class", f"{ style_class } not-rounded")
            button.setFixedHeight(button_height)
            container_buttons_layout.addWidget(button)

        button_save = CustomQPButton(text="Guardar", on_click=lambda: print("save!"))
        button_cancel = CustomQPButton(
            text="Cancelar", on_click=lambda: print("cancel!")
        )

        # container_buttons_layout.addWidget(button_save)
        # container_buttons_layout.addWidget(button_cancel)

        # self.container_buttons.setFixedHeight(
        #     button_save.height() + button_cancel.height()
        # )

        self.container_buttons.setFixedHeight(len(buttons) * button_height)

        self.main_layout.addWidget(self.container_buttons)

        return

    def handle_change_combobox(self, value):
        if value == self.default_prompt:
            return

        print(f"combobox change: { value }")
        self.update_prompt = value

    def handle_click_save(self):
        if (
            not hasattr(self, "update_prompt")
            or self.default_prompt == self.update_prompt
        ):
            return

        res = self.config.update_property("expert", self.update_prompt)
        print(res)

        toasts().success("¡Experto actualizado con éxito!")

        self.close()

        return

    def update_height(self):
        print(self.container_buttons.height())
        self.main_layout.setSpacing(20)

        self.setFixedHeight(
            self.container_prompts.height() + self.container_buttons.height() + 20
        )
        return

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
