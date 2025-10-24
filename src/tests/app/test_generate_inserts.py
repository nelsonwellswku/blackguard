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

import pytest
from app.database.database_config import DatabaseConfig
from app.database.engine import create_engine
from app.generate_inserts import generate_inserts

test_db = DatabaseConfig("SA", "superSecret123!", "127.0.0.1", "Northwind")


@pytest.mark.only
def test_generate_inserts_for_a_single_table():
    engine = create_engine(test_db)

    select = """
select
Region.RegionID Region__RegionID,
Region.RegionDescription Region__RegionDescription
from Region;
"""

    with engine.connect() as connection:
        inserts = generate_inserts(select, connection)

    assert inserts
    assert inserts == [
        "insert into Region (RegionID, RegionDescription) VALUES (1, 'Eastern')",
        "insert into Region (RegionID, RegionDescription) VALUES (2, 'Western')",
        "insert into Region (RegionID, RegionDescription) VALUES (3, 'Northern')",
        "insert into Region (RegionID, RegionDescription) VALUES (4, 'Southern')",
    ]
