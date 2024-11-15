from datetime import datetime


def current_datetime():
    return str(datetime.now()).split(".")[0].replace(":", "")
