import base64
from io import BytesIO
import pyautogui as pg


# Toma la captura de pantalla y retorna el path y el base64
def take_ss():
    try:

        ss = pg.screenshot()  # pyautogui

        output = BytesIO()
        ss.save(output, format="PNG")

        ss_data = output.getvalue()
        ss_base64 = base64.standard_b64encode(ss_data).decode("utf-8")

        return ss_base64, "image/png"

    except Exception as e:
        print(f"Error: {e}")