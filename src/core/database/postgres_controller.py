import psycopg2
from psycopg2.extras import DictCursor

from ...utils import log
from ...settings import DB_HOST, DB_NAME, DB_PASS, DB_USER


class ControllerPostgres:
    def __init__(self, table) -> None:
        self.table = table
        self.connection = None
        self.cursor = None
        self.columns: list = None
        self.values: list = None
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        )
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def manual(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor

    def load(self, condition=None, selector="*", join=False, table=None, inner=None):
        self.table = table
        query = f"SELECT {selector} FROM {self.table} {self._inner_join(inner)} {self._condition_parser(condition)}"
        self.cursor.execute(query)
        cursor_data = self.cursor.fetchall()
        cursor_data = sum(cursor_data, []) if join else cursor_data

        self.connection.commit()

        return cursor_data

    def insert(self, values, columns="", table=None, inner=None) -> None:
        self.table = table
        self.values = values
        if columns:
            self.columns = columns
            len_condition = self._correct_columns_len()

            if not len_condition:
                return

            columns = f"({', '.join(self.columns)})"

        values = ", ".join([self.is_values(value) for value in values])

        query = f"INSERT INTO {self.table} {columns} VALUES({values})"
        try:
            self.cursor.execute(query)
        except psycopg2.errors.UniqueViolation:
            return log((["b", "f"], "unique values"))

        self.connection.commit()

    def update(self, columns, values, condition=None, table=None, inner=None) -> None:
        self.table = table
        self.columns = columns
        self.values = values
        len_condition = self._correct_columns_len()

        if not len_condition:
            return

        values = [self.is_values(value) for value in self.values]

        ziped = [
            f"{column} = {value}" for column, value in zip(self.columns, self.values)
        ]

        query = f"UPDATE {self.table} SET {', '.join(ziped)} {self._update_inner(inner)} {self._condition_parser(condition, not bool(inner))}"
        self.cursor.execute(query)

        self.connection.commit()

    def _update_inner(self, inner):
        if not inner:
            return ""
        if not isinstance(inner, tuple):
            return ""

        return f"FROM {inner[0]} WHERE {self.table}.{inner[1]} = {inner[0]}.{inner[1]} and "

    def _condition_parser(self, condition, with_where=True):
        prefix = "WHERE"
        if not condition:
            return ""
        if not with_where:
            prefix = ""
        return f"{prefix} {condition}"

    def _correct_columns_len(self) -> bool:
        condition = True
        if len(self.columns) != len(self.values):
            condition = False

        return condition

    def _inner_join(self, inner):
        if not inner:
            return ""
        if not isinstance(inner, tuple):
            return ""

        return f"INNER JOIN {inner[0]} ON {self.table}.{inner[1]}={inner[0]}.{inner[1]}"

    def is_values(self, value):
        if isinstance(value, str):
            return f"'{value}'"

        return f"{value}"

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        if value:
            self._table = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        if value:
            if not isinstance(value, list):
                self._columns = [value]
            else:
                self._columns = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        if value:
            if not isinstance(value, list):
                self._values = [value]
            else:
                self._values = value
