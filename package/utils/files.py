import os
import json
import base64
from package.core.constants import config_path, extensions_media


def open_file(path=None, mode="r", content=None):
    try:
        if path is None:
            raise Exception("Path is invalid!")

        if mode == "w" and content is None:
            raise Exception("The content is invalid!")

        with open(path, mode) as file:
            if mode == "w":
                file.write(content)
                return True

            return file.read()

    except Exception as e:
        print("Error: ", e)
        return


def encode_to_base64(fileName):
    file_content = open_file(fileName, mode="rb")

    if file_content is None:
        return

    file_extension = os.path.splitext(fileName)[1]

    base64_bytes = base64.standard_b64encode(file_content)
    base64_string = base64_bytes.decode("utf-8")

    extension = extensions_media[file_extension]

    url = f"data:{extension};base64,{base64_string}"

    return {"media_type": extension, "data": base64_string}


class HandleJson:
    def __init__(self, path: str = "settings.json") -> None:
        self.path = path

        self.data = self.file("r")

    def file(self, mode: str = "r"):
        try:
            with open(self.path, mode, encoding="utf-8") as file:
                if mode == "w":
                    return json.dump(self.data, file, indent=4, ensure_ascii=False)

                data = json.load(file)

            return dict(data)
        except Exception as e:
            print(e)
            return {}

    # NOTE: para no generar confusión con "w" en cada llamada a self.file
    def update_file(self):
        return self.file("w")

    def get_value(self, key: str = "path_ss"):
        try:
            # if key in self.data is False:
            if not self.__exists_key(key):
                raise KeyError(f"La clave {key} no se encuentra en el json.")

            return self.data[key]

        except Exception as e:
            print(e)

            return str(e)

    def add_property(self, key: str, value: str):
        try:
            self.data[key] = value
            self.update_file()

        except KeyError as e:
            print(e)

    def update_property(self, key: str, new_value: str):
        try:
            if not self.__exists_key(key):
                print("prop not exists")
                return

            self.data[key] = new_value
            self.update_file()

            return True

        except KeyError as e:
            print(e)

    def delete_property(self, key: str):
        try:
            del self.data[key]
            self.update_file()

        except KeyError as e:
            print(e)

    def __exists_key(self, key: str):
        return key in self.data


settings = HandleJson(config_path)