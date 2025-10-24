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

import argparse
from logging import getLogger
import logging

from app.database.database_config import DatabaseConfig
from app.generate_inserts import generate_inserts
from app.generate_select import generate_select
from app.database.engine import create_engine

logging.basicConfig(level=logging.DEBUG)

logger = getLogger(__name__)
parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", default="SA")
parser.add_argument("-p", "--password", default="superSecret123!")
parser.add_argument("-c", "--hostname", default="127.0.0.1")
parser.add_argument("-d", "--database", default="Northwind")


def main():
    args = parser.parse_args()

    logger.info("Connecting to database.")

    engine = create_engine(
        DatabaseConfig(args.username, args.password, args.hostname, args.database)
    )

    with engine.connect() as connection:
        selects = generate_select([], connection)
        inserts = generate_inserts(selects, connection)

    logger.info("Writing insert statements to inserts.sql.")
    with open("inserts.sql", "w") as file:
        file.writelines(f"{statement}\n" for statement in inserts)

    logger.info("Finished.")


if __name__ == "__main__":
    main()
