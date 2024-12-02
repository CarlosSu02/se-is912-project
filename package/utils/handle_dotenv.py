from io import StringIO
import os

from dotenv import load_dotenv, dotenv_values
import re

from package.ui.toast_manager import toasts
from package.utils.files import open_file


clients = {
    "Claude": "API_KEY_CLAUDE",
    # "ChatGPT": "API_KEY_CHATGPT",
    # "Gemini": "API_KEY_GEMINI",
}

regex = r"^sk-[a-zA-Z0-9_-]{32,}$"


def exists_dotenv():
    if not os.path.exists(".env"):
        open(".env", "w").close()

    return load_dotenv()


def data_env(file=".env"):
    return dotenv_values(file)


def get_env(name):
    return data_env()[name]


def set_env(key, value):
    if key is None or value is None:
        return

    # config = StringIO(f"{ key }={ value }")
    # load_dotenv(stream=config)

    open_file(path=".env", mode="w", content=f"{ key }={ value }")

    # The error is handling in open_file function
    toasts().success("Se agregó la API Key al archivo .env.")

    return


def validate_key(value=""):
    return re.match(regex, value, re.MULTILINE)
