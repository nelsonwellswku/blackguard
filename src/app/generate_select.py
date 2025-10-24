# Blackguard - Generate SQL insert statements for test data
# Copyright (C) 2025 Nelson Wells

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pprint import pprint
from sqlalchemy import Connection, text
from collections import OrderedDict

get_columns_query = text("""
SELECT c.COLUMN_NAME column_name
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE TABLE_NAME = :table_name
""")

template = """
select
{columns}
from {table};
"""

def generate_select(tables: list[str], connection: Connection) -> str:
    generated_queries = []
    for table in tables:
        rows = connection.execute(get_columns_query, { "table_name": table}).mappings().fetchall()
        column_names = [row["column_name"] for row in rows]
        selects = [f"{column_name} {table}__{column_name}" for column_name in column_names]
        generated_query = template.replace("{columns}", str.join(",\n", selects))
        generated_query = generated_query.replace("{table}", table)
        generated_queries.append(generated_query.strip())

    return generated_queries[0]
