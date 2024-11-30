# import pyautogui as pg # if not use wsl, uncomment this line.

# from package.utils.date import current_datetime
import base64
from io import BytesIO
import os
from sys import exception
from package.utils.date import current_datetime
from package.utils.path import folder_exists
from package.utils.files import settings

# path_ss = r"./scs"


def take_ss(e):
    try:
        import pyautogui as pg  # if use wsl, else comment this line. Message terminal => NOTE: You must install tkinter on Linux to use MouseInfo. Run the following: sudo apt-get install python3-tk python3-devuu

        path_ss = settings.get_value("path_ss")

        ss = pg.screenshot()
        # path = f"{path_ss}/Screenshot {current_datetime()}.png"
        #
        # if not folder_exists(path_ss):
        #     os.makedirs(path_ss)
        #
        # ss.save(path)

        output = BytesIO()
        ss.save(output, format="PNG")

        ss_data = output.getvalue()
        ss_base64 = base64.standard_b64encode(ss_data).decode("utf-8")

        url = f"data:image/png;base64,{ ss_base64 }"

        # with open("./ss.txt", "w") as f:
        #     f.write(url)

        return url

    except Exception as e:
        print(f"Error: { e }")
