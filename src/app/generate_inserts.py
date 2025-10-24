from dataclasses import dataclass
from pprint import pprint
from typing import Any
from sqlalchemy import Connection, RowMapping, text


def flatten_recursive(nested_list):
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten_recursive(item)
        else:
            yield item


class Inserter:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns = []
        self.values = []

    def add(self, column: str, value: Any):
        self.columns.append(column)
        self.values.append(value)

    def get_insert_statement(self):
        columns = str.join(", ", self.columns)

        def format(v: Any):
            if isinstance(v, str):
                return f"'{v}'"
            else:
                return str(v)

        values = str.join(", ", [format(value) for value in self.values])

        return f"insert into {self.table_name} ({columns}) VALUES ({values})"


class Container:
    _insert_template = """INSERT INTO {table} ()"""

    def __init__(self, row: RowMapping):
        table_dict: dict[str, Inserter] = {}
        for alias_column_name in row:
            (table, column) = alias_column_name.split("__")
            value = row[alias_column_name]
            if table not in table_dict:
                table_dict[table] = Inserter(table)
            table_dict[table].add(
                column, value.strip() if isinstance(value, str) else value
            )
        self._table_dict = table_dict

    def get_inserts(self):
        return [
            inserter.get_insert_statement() for inserter in self._table_dict.values()
        ]


def generate_inserts(select: str, connection: Connection):
    query_results = connection.execute(text(select)).mappings().fetchall()
    inserts = list(
        flatten_recursive([Container(row).get_inserts() for row in query_results])
    )
    return inserts
