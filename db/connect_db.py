import os
import re
import sqlite3
from package.utils.files import open_file


class ConnectDB:
    _folder = "./db/data"
    _path_db = f"{_folder}/widget.db"

    def __init__(self):
        # print(self._path_db)

        # create folder
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

            # create file
            # if not os.path.exists(self._path_db):
            open(self._path_db, "w").close()

    def connection(self):
        try:
            connection = sqlite3.connect(self._path_db, timeout=10)
            connection.execute("PRAGMA journal_mode=WAL;")

            return connection

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return

    def close(self, conn):
        conn.close()

    def init_tables(self):
        try:
            conn = self.connection()

            if conn is None:
                raise sqlite3.Error(
                    "No se pudo establecer la conexión a la base de datos."
                )

            cursor = conn.cursor()

            query = open_file("./db/queries/init.sql", "r")

            if query is None:
                raise sqlite3.Error("Error al obtener el query.")

            for table in str(query).replace("\n", "").split(";"):
                if re.match(r"CREATE", table, re.MULTILINE):
                    cursor.execute(table)

            conn.commit()

            cursor.close()
            self.close(conn)

        except sqlite3.Error as err:
            print(f"Error: {err}")