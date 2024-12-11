from .enums import ClientsEnum, Table

clients = {c.name: c.value for c in ClientsEnum}

tables = [t.value for t in Table]

config_path = "./config/settings.json"

extensions_media = {
    ".ico": "image/x-icon",
    ".jpg": "image/jpg",
    ".png": "image/png",
    ".bmp": "image/bmp",
    ".pdf": "application/pdf",
}