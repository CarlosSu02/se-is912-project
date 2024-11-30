from package.utils.files import open_file


def get_stylesheet(name="styles"):
    content = open_file(f"./styles/{name}.css")
    return content
