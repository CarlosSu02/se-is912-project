import typing
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from package.ui.custom_button import CustomQPButton
from package.ui.styles import get_stylesheet
from package.ui.toast_manager import toasts
from package.utils.files import HandleJson


class QuestionWindow(QWidget):
    def __init__(self, parent, window_key):
        super().__init__()

        self.parent = parent
        self.window_key = window_key

        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet(get_stylesheet())

        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 140)
        self.setWindowTitle("Pregunta")
        # self.setFont(QFont("Arial", 12))
        self.setObjectName("question-window")

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.prompts()
        self.textarea()
        self.buttons()

        # self.main_layout.addStretch(0)

        self.update_height()

        return

    def prompts(self):
        prompts = HandleJson("./config/prompts.json")
        # self.config = HandleJson(config_path)

        if prompts.data is None:
            return

        self.prompts_file = prompts

        # dict_keys = type(dict[str, str]().keys())
        self.items_combobox: list[str] = list(prompts.data.keys())
        # self.default_prompt = self.config.get_value("expert")

        # print(len(prompts.data.keys()))
        # print(list(prompts.data.keys()))
        # print(", ".join(prompts.data.keys()))

        # label = QLabel(", ".join(prompts.data.keys()))

        self.container_prompts = QWidget()
        container_layout = QVBoxLayout(self.container_prompts)

        label = QLabel("Experto", self)
        # label.setFont(QFont("Arial", 12))
        # label.move(20, 50)

        combobox = QComboBox()
        combobox.addItems(prompts.data.keys())
        # combobox.setFont(QFont("Arial", 12))
        # combobox.setFixedSize(self.width(), 30)
        # combobox.resize(combobox.sizeHint())
        # combobox.move(90, 50)
        combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        combobox.setFixedHeight(40)

        # combobox.setCurrentIndex(self.items_combobox.index(self.default_prompt))

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
        # combobox.currentTextChanged.connect(lambda value: self.current_prompt = value)

        container_layout.addWidget(label)
        container_layout.addWidget(combobox)
        self.container_prompts.setFixedHeight(label.height() + combobox.height() + 5)

        # self.main_layout.addLayout(container_layout)
        self.main_layout.addWidget(self.container_prompts)
        self.main_layout.addStretch(0)

        self.current_prompt = combobox.currentText()

    def textarea(self):
        self.container_textarea = QWidget()
        container_textarea_layout = QVBoxLayout(self.container_textarea)

        # label
        label = QLabel("Ingresa una pregunta", self)

        # Textarea
        self.question_area = QPlainTextEdit()
        self.question_area.setPlaceholderText("¿Qué es un Sistema Experto?")
        self.question_area.setFixedHeight(225)
        self.question_area.setProperty("class", "textarea")

        self.question_area.textChanged.connect(self.handle_text_changed)

        container_textarea_layout.addWidget(label)
        container_textarea_layout.addWidget(self.question_area)

        self.container_textarea.setFixedHeight(
            label.height() + self.question_area.height() + 10
        )

        # self.container_textarea.setStyleSheet("background-color: red;")

        self.container_textarea.setProperty("class", "qa-bg")
        self.main_layout.addWidget(self.container_textarea)

        # self.main_layout.addWidget(self.question_area)

        # self.main_layout.addStretch(0)

        return

    def buttons(self):
        self.container_buttons = QWidget()
        container_buttons_layout = QHBoxLayout(self.container_buttons)

        container_buttons_layout.addStretch()

        # buttons = [
        #     ("Enviar", "qa-save", self.handle_send),
        #     ("Cerrar", "qa-close", self.close),
        # ]
        button_height = 40

        # for name, style_class, fn in buttons:
        #     print(name, style_class)
        #     button = CustomQPButton(text=name, on_click=fn)
        #     # button.setObjectName("not-rounded")
        #     # button.setProperty("class", "not-rounded")
        #     # button.setProperty("class", style_class)
        #     button.setProperty("class", f"{ style_class } not-rounded")
        #     button.setFixedHeight(button_height)
        #     # button.setFixedWidth(100)
        #     container_buttons_layout.addWidget(button)

        # button_save
        self.button_save = CustomQPButton(text="Enviar", on_click=self.handle_send)
        self.button_save.setProperty("class", "qa-save not-rounded")
        self.button_save.setEnabled(False)

        button_cancel = CustomQPButton(text="Cancelar", on_click=self.close)
        button_cancel.setProperty("class", "qa-cancel not-rounded")

        container_buttons_layout.addWidget(self.button_save)
        container_buttons_layout.addWidget(button_cancel)

        # self.container_buttons.setFixedHeight(
        #     button_save.height() + button_cancel.height()
        # )

        container_buttons_layout.setContentsMargins(10, 20, 10, 10)

        self.container_buttons.setFixedHeight(2 * button_height)

        self.main_layout.addWidget(self.container_buttons)

        return

    def handle_change_combobox(self, value):
        self.current_prompt = value

    def handle_text_changed(self):
        value = self.question_area.toPlainText().strip()

        condition = len(value) < 10

        # if len(value) < 10:
        #     return

        self.button_save.setEnabled(not condition)

    def handle_send(self):
        print(self.question_area.toPlainText())
        print(self.current_prompt)

        question = self.question_area.toPlainText()
        prompt = self.current_prompt

        print(self.prompts_file.get_value(prompt))

        toasts().success(f"Prompt: { prompt }, Pregunta: { question }")

    def update_height(self):
        self.main_layout.setSpacing(20)

        new_h = (
            self.container_prompts.height()
            + self.container_textarea.height()
            + self.container_buttons.height()
            + 20
        )

        self.setFixedHeight(new_h)

        return

    def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
        if not hasattr(self.parent, "windows") or not isinstance(self.parent, QWidget):
            return

        self.parent.handle_windows(self.window_key)

        return super().closeEvent(a0)
