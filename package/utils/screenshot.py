import base64
from io import BytesIO


def take_ss():
    try:
        import pyautogui as pg

        ss = pg.screenshot()

        output = BytesIO()
        ss.save(output, format="PNG")

        ss_data = output.getvalue()
        ss_base64 = base64.standard_b64encode(ss_data).decode("utf-8")

        url = f"data:image/png;base64,{ss_base64}"

        # with open("./ss.txt", "w") as f:
        #     f.write(url)

        return {"data": ss_base64, "media_type": "image/png"}

    except Exception as e:
        print(f"Error: {e}")