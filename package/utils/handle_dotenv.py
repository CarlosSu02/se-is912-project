import os
import re
from dotenv import load_dotenv, dotenv_values
from package.core.constants import clients
from . import open_file

regex = r"^sk-[a-zA-Z0-9_-]{32,}$"


def exists_dotenv():
    if not os.path.exists(".env"):
        open(".env", "w").close()

    return load_dotenv()


def data_env(file=".env"):
    exists_dotenv()
    return dotenv_values(file)


def get_env(name=None):
    data = data_env()

    if len(data) == 0:
        return

    return data[name] if name is not None else list(data)[0]


def set_env(key, value):
    if key is None or value is None:
        return

    set = open_file(path=".env", mode="w", content=f"{key}={value}")

    return bool(set)


def delete_key(key):
    try:
        if key is None:
            return

        open(".env", "w").close()  # lo recrea de nuevo

        return True

    except Exception as e:
        print(f"Error: {e}")
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