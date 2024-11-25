# import pyautogui as pg # if not use wsl, uncomment this line.

# from package.utils.date import current_datetime
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
        path = f"{path_ss}/Screenshot {current_datetime()}.png"

        if not folder_exists(path_ss):
            os.makedirs(path_ss)

        ss.save(path)

    except Exception as e:
        print(f"Error: { e }")
