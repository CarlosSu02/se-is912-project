from enum import Enum


class ClientsEnum(Enum):
    Claude = "API_KEY_CLAUDE"
    # ChatGPT = "API_KEY_CHATGPT"
    # Gemini = "API_KEY_GEMINI"


class Icon(Enum):
    WIDGET = "widget.svg"
    TRASH = "trash.svg"
    QUESTION = "user-question-alt.svg"
    PDF = "file-pdf.svg"
    IMAGE = "file-image.svg"
    SS = "screenshot.svg"
    CLOSE = "close.svg"
    CHART = "chart.svg"
    KEY = "key.svg"