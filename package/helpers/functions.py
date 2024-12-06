# Functions with speech


from pyqttoast.os_utils import os
from package.helpers.screenshot import take_ss
from package.ui.toast_manager import toasts
from package.utils.files import encode_to_base64
from package.helpers.clients import current_client, vision_clients


def handle_req_screeshot():
    try:
        info = take_ss()

        if info is None:
            return

        res = vision_clients[str(current_client)](
            image_media_type=info["media_type"], base64_string=info["data"]
        )

        return res

    except Exception as e:
        toasts().error(e)
        return


def handle_req_files(fileName):
    try:
        file_base64 = handle_load_file(fileName)

        if file_base64 is None:
            return

        return file_base64

    except Exception as e:
        toasts().error(e)


def handle_req_document():
    try:
        pass
    except Exception as e:
        toasts().error(e)


def handle_req_question():
    try:
        pass
    except Exception as e:
        toasts().error(e)


# Manejo de archivos general para no repetir codigo
def handle_load_file(fileName):
    if not fileName:
        return

    try:
        file_name = os.path.basename(fileName)
        toasts().info(file_name)

        base64 = encode_to_base64(fileName)

        return base64

    except Exception as e:
        toasts().error(str(e))
        return
