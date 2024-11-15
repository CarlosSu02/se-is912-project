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

            # print("Content", file.read())
            return file.read()

    except Exception as e:
        print("Error: ", e)
        return f"Error: {e}"
