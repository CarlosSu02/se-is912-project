import sqlite3
import pandas as pd
from db.connect_db import ConnectDB
from package.helpers.clients import current_client
from package.core.enums import Table

_get_data_query = "SELECT * FROM questions_responses;"


class TQuestion:

    def get_data():
        try:
            conn = ConnectDB().connection()

            if conn is None:
                raise sqlite3.Error(
                    "No se pudo establecer la conexión a la base de datos."
                )

            cursor = conn.cursor()

            cursor.execute(_get_data_query)

            res = cursor.fetchall()

            cursor.close()
            conn.close()

            return res

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return

    def get_data_pandas():
        try:

            conn = ConnectDB().connection()

            if conn is None:
                raise sqlite3.Error(
                    "No se pudo establecer la conexión a la base de datos."
                )

            df = pd.read_sql_query(_get_data_query, conn)
            df.name = Table.QUESTIONS.value

            conn.close()

            return df

        except Exception as e:
            print(f"Error: {e}")
            return

    def add_element(expert=None, question=None, response=None, client=current_client):
        try:
            if expert is None or question is None or client is None:
                raise ValueError("Los valores no pueden ser None.")

            conn = ConnectDB().connection()

            if conn is None:
                raise sqlite3.Error(
                    "No se pudo establecer la conexión a la base de datos."
                )

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO questions_responses (expert, question, response, client) VALUES(?, ?, ?, ?)",
                (expert, question, response, client),
            )

            conn.commit()

            cursor.close()
            conn.close()

            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return