import os
import sqlite3


class ConnectDB:
    _path_db = "./db/data/test.db"

    def __init__(self):
        print(">?")

        # create file
        # if not os.path.exists(self._path_db):
        #     open(self._path_db, "w").close()

    def connection(self):
        connection = sqlite3.connect(self._path_db, timeout=10)
        connection.execute("PRAGMA journal_mode=WAL;")

        return connection

    # def cursor(self):
    #     self.cursor

    def close(self, conn):
        conn.close()

    def test(self):
        conn = self.connection()

        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS stocks
            (date text, trans text, symbol text, qty real, price real)"""
        )

        # Insert a row of data
        cursor.execute(
            "INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)"
        )

        # Save (commit) the changes
        conn.commit()

        # Close the connection
        self.close(conn)
