from .enums import ClientsEnum, Table

clients = {c.name: c.value for c in ClientsEnum}

tables = [t.value for t in Table]

config_path = "./config/settings.json"

extensions_media = {
    ".ico": "image/x-icon",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".bmp": "image/bmp",
    ".pdf": "application/pdf",
}


class FunctionCall:
    def __init__(self, fn, params):

        self.fn = fn
        self.params = params

    def exec(self):
        if not isinstance(self.params, (list, tuple)):
            self.params = [self.params]

        return self.fn(*self.params)

    def save(self, res):
        if not isinstance(self.params, (list, tuple)):
            self.params = [self.params]

        return self.fn(*self.params, res)