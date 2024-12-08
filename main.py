if __name__ == "__main__":
    import sys
    from package.app import app
    from db.connect_db import ConnectDB

    db = ConnectDB()
    db.init_tables()

    sys.exit(app.exec())
