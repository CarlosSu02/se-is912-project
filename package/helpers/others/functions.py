# Functions with speech


from pyqttoast.os_utils import os
from db.media_db import TMedia
from db.question_db import TQuestion
from package.core.constants import FunctionCall
from package.utils import take_ss, encode_to_base64
from package.ui.dialogs.toast_manager import toasts
from package.helpers.clients import (
    current_client,
    vision_clients,
    text_clients,
    documents_clients,
)
from package.core.enums import MediaType


def handle_req_screenshot(data, media_type):
    try:
        # info = take_ss()

        if data is None or media_type is None:
            return

        base = vision_clients[str(current_client)](
            image_media_type=media_type, base64_string=data
        )

        # TMedia.add_element(type=MediaType.SCREENSHOT, response=res)

        return *base, FunctionCall(TMedia.add_element, MediaType.SCREENSHOT)

    except Exception as e:
        toasts().error(e)
        print(e)
        return


def handle_req_files_media(fileName):
    try:
        info = handle_load_file(fileName)

        if info is None:
            raise Exception("No se seleccionó un archivo multimedia.")

        res = vision_clients[str(current_client)](
            image_media_type=info["media_type"], base64_string=info["data"]
        )

        # TMedia.add_element(type=MediaType.IMAGE, response=res)

        return *res, FunctionCall(TMedia.add_element, MediaType.IMAGE)

    except Exception as e:
        # toasts().error(e)
        raise Exception(e)


def handle_req_document(fileName):
    try:
        info = handle_load_file(fileName)

        if info is None:
            raise Exception("No se seleccionó un PDF.")

        base = documents_clients[str(current_client)](
            document_media_type=info["media_type"], base64_string=info["data"]
        )

        # TMedia.add_element(type=MediaType.DOCUMENT, response=res)

        return *base, FunctionCall(TMedia.add_element, MediaType.DOCUMENT)

    except Exception as e:
        # toasts().error(e)
        raise Exception(e)


def handle_req_question(expert, prompt, text):
    try:
        base = text_clients[str(current_client)](prompt, text)

        # TQuestion.add_element(expert, text)

        return *base, FunctionCall(TQuestion.add_element, (expert, text))

    except Exception as e:
        # toasts().error(e)
        raise Exception(e)


# Manejo de archivos general para no repetir codigo
def handle_load_file(fileName):
    if not fileName:
        return

    try:
        file_name = os.path.basename(fileName)
        # toasts().info(file_name)

        data = encode_to_base64(fileName)

        return data

    except Exception as e:
        # toasts().error(str(e))
        raise Exception(e)