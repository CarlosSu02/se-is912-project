import os
import base64

extensions = {
    ".ico": "image/x-icon",
    ".jpg": "image/jpg",
    ".png": "image/png",
    ".bmp": "image/bmp",
}


def open_file(path=None, mode="r", content=None):
    try:
        if path is None:
            raise Exception("Path is invalid!")

        if mode == "w" and content is None:
            raise Exception("The content is invalid!")

        with open(path, mode) as file:
            if mode == "w":
                file.write(content)
                return

            return file.read()

    except Exception as e:
        print("Error: ", e)
        # return f"Error: {e}"
        return


def encode_to_base64(fileName):
    file_content = open_file(fileName, mode="rb")

    if file_content is None:
        return

    file_extension = os.path.splitext(fileName)[1]

    base64_bytes = base64.standard_b64encode(file_content)
    base64_string = base64_bytes.decode("utf-8")

    url = f"data:{extensions[file_extension]};base64,{base64_string}"

    return url
