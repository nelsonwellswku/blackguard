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

from logging import getLogger
from sqlalchemy import URL
from sqlalchemy.engine import create_engine as sql_alchemy_create_engine

logger = getLogger(__name__)


def create_engine(username: str, password: str, hostname: str, database: str):
    connection_url = URL.create(
        "mssql+pyodbc",
        username=username,
        password=password,
        host=hostname,
        port=1433,
        database=database,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
        },
    )

    engine = sql_alchemy_create_engine(connection_url)
    return engine
