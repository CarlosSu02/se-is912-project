from enum import Enum


class ClientsEnum(Enum):
    Claude = "API_KEY_CLAUDE"
    # ChatGPT = "API_KEY_CHATGPT"
    # Gemini = "API_KEY_GEMINI"


clients = {c.name: c.value for c in ClientsEnum}
