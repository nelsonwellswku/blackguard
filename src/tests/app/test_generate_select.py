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

from dataclasses import dataclass
from app.database.engine import create_engine
from app.generate_select import generate_select


@dataclass
class DatabaseConfig:
    username: str
    password: str
    hostname: str
    database: str


test_db = DatabaseConfig("SA", "superSecret123!", "127.0.0.1", "Northwind")


def test_generate_select_with_one_table():
    engine = create_engine(
        test_db.username, test_db.password, test_db.hostname, test_db.database
    )

    with engine.connect() as connection:
        actual = generate_select(["Region"], connection)

    expected = """
select
RegionID Region__RegionID,
RegionDescription Region__RegionDescription
from Region;
    """.strip()
    assert actual == expected
