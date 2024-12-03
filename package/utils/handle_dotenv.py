import os
import re
from dotenv import load_dotenv, dotenv_values
from package.constants.various import clients
from package.utils.files import open_file


# clients = {
#     "Claude": "API_KEY_CLAUDE",
#     # "ChatGPT": "API_KEY_CHATGPT",
#     # "Gemini": "API_KEY_GEMINI",
# }

""" 
# Alternativa para no repetir codigo
from enum import Enum

class Clients(Enum):
    Claude = "API_KEY_CLAUDE"
    ChatGPT = "chatgpt"

clients = { c.name: c.value for c in Clients }

print(list(Clients))
print(clients)

class Clients2(Enum):
    CLAUDE = 'Claude', 'key'
    CHATGPT = "chatgpt", 'name'

print({ list(t.value)[0]: list(t.value)[1] for t in Clients2 })
"""

regex = r"^sk-[a-zA-Z0-9_-]{32,}$"


def exists_dotenv():
    if not os.path.exists(".env"):
        open(".env", "w").close()

    return load_dotenv()


def data_env(file=".env"):
    return dotenv_values(file)


def get_env(name=None):
    data = data_env()
    return data[name] if name is not None else list(data)[0]


def set_env(key, value):
    if key is None or value is None:
        return

    # config = StringIO(f"{ key }={ value }")
    # load_dotenv(stream=config)

    set = open_file(path=".env", mode="w", content=f"{ key }={ value }")

    # The error is handling in open_file function
    # toasts().success("Se agregó la API Key al archivo .env.")

    return bool(set)


def delete_key(key):
    try:
        if key is None:
            return

        open(".env", "w").close()  # lo recrea de nuevo

        return True

    except Exception as e:
        print(f"Error: { e }")
        return False


def validate_key(value=""):
    return re.match(regex, value, re.MULTILINE)


def key_from_value(value):
    if value is None:
        return

    keys = list(clients.keys())
    current_key = None

    for key in keys:
        if clients[key] == value:
            current_key = key
            break

    return current_key
