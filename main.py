from db.connect_db import ConnectDB


if __name__ == "__main__":
    import sys
    from package.app import app

    db = ConnectDB()
    db.test()
    sys.exit(app.exec())
