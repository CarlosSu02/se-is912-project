import typing
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from package.helpers.others.functions import handle_req_question
from package.ui.components import CustomQPButton
from package.ui.styles import get_stylesheet
from package.utils import HandleJson


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

        self.update_height()

        return

    def prompts(self):
        prompts = HandleJson("./config/prompts.json")

        if prompts.data is None:
            return

        self.prompts_file = prompts

        # dict_keys = type(dict[str, str]().keys())
        self.items_combobox: list[str] = list(prompts.data.keys())

        self.container_prompts = QWidget()
        container_layout = QVBoxLayout(self.container_prompts)

        label = QLabel("Experto", self)
        # label.setFont(QFont("Arial", 12))

        combobox = QComboBox()
        combobox.addItems(prompts.data.keys())
        # combobox.setFont(QFont("Arial", 12))

        combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        combobox.setFixedHeight(40)

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

        self.container_textarea.setProperty("class", "qa-bg")
        self.main_layout.addWidget(self.container_textarea)

        return

    def buttons(self):
        self.container_buttons = QWidget()
        container_buttons_layout = QHBoxLayout(self.container_buttons)

        container_buttons_layout.addStretch()

        button_height = 40

        # button_save
        self.button_save = CustomQPButton(text="Enviar", on_click=self.handle_send)
        self.button_save.setProperty("class", "qa-save not-rounded")
        self.button_save.setEnabled(False)

        button_cancel = CustomQPButton(text="Cancelar", on_click=self.close)
        button_cancel.setProperty("class", "qa-cancel not-rounded")

        container_buttons_layout.addWidget(self.button_save)
        container_buttons_layout.addWidget(button_cancel)

        container_buttons_layout.setContentsMargins(10, 20, 10, 10)

        self.container_buttons.setFixedHeight(2 * button_height)

        self.main_layout.addWidget(self.container_buttons)

        return

    def handle_change_combobox(self, value):
        self.current_prompt = value

    def handle_text_changed(self):
        value = self.question_area.toPlainText().strip()

        condition = len(value) < 10

        self.button_save.setEnabled(not condition)

    def handle_send(self):
        print(self.question_area.toPlainText())
        print(self.current_prompt)

        question = self.question_area.toPlainText()
        expert = self.current_prompt
        prompt = self.prompts_file.get_value(expert)

        # print(self.prompts_file.get_value(prompt))
        self.close()

        # toasts().success(f"Prompt: { prompt }, Pregunta: { question }")

        text = handle_req_question(expert, prompt, question)

        if not hasattr(self.parent, "handle_speech") or not isinstance(
                self.parent, QWidget
        ):
            return

        self.parent.handle_speech(text)

        return

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