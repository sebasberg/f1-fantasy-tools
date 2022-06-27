from constants import DATABASE_NAME
import sqlite3
import os

class DatabaseHelper:

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath("database/database_helper.py"))
        db_path = os.path.join(BASE_DIR, DATABASE_NAME)
        self._connection = sqlite3.connect(db_path)
        self._cursor = self.connection.cursor()

    # To support open database using "with" statement
    def __enter__(self):
        return self

    # To support open database using "with" statement
    def __exit__(self, exception_type, exception_value, trace):
        self.close()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.cursor.close()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def tuple_to_dict(self, query_result):
        result_dict = {}
        for tuple in query_result:
            result_dict[tuple[0]] = tuple[1:]
        return result_dict

    def get_drivers(self):
        sql = "SELECT * FROM drivers"
        return self.tuple_to_dict(self.query(sql))

    def get_driver_price(self, driver):
        sql = "SELECT price FROM drivers WHERE initials = ?"
        self.execute(sql, (driver,))
        return self.fetchone()[0]

    def get_driver_points(self, driver):
        return

    def get_constructors(self):
        sql = "SELECT * FROM constructors"
        return self.tuple_to_dict(self.query(sql))

    def get_constructor_price(self, constructor):
        sql = "SELECT price FROM constructors WHERE abbreviation = ?"
        self.execute(sql, (constructor,))
        return self.fetchone()[0]

    def get_constructor_points(self, constructor):
        return