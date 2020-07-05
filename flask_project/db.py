"""
Name of file - db.py

Purpose of file - This file is a rough demonstration of how a developer
could create a database like ours using a python script. I created our database using the sqlite3 terminal (and SQL commands) because using that was faster than debugging a python script.

Date of most recent revision - 6/1/20

Author(s) - Ethan Bradway

Dependencies - sqlite3
"""

import sqlite3
from sqlite3 import Error


def create_connection(db_file: str) -> sqlite3.Connection:
    """
    Parameters - A file path corresponding to a database.

    Return Data - A Connection object.

    Purpose - This method creates a connection to the database specified in the provided file path for later use.

    Pre-conditions and post-conditions - N/A
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def create_table(conn, sqlst_create_table):
    """
    Parameters - A Connection object and a prepared SQL statement to execute as a string.

    Return Data - N/A

    Purpose - This function executes the SQL statement provided to create a table.

    Pre-conditions and post-conditions - N/A
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sqlst_create_table)
    except Exception as e:
        print(e)


def main():
    """
    Parameters - N/A

    Return Data - N/A

    Purpose - This method creates a namespace for this script to operate in.

    Pre-conditions and post-conditions - N/A
    """
    database = r"test2.db"

    sql_create_new_table = """ create table if not exists examplePeriodicTable (
                                   elementName text not null,
                                   atomicSymbol text not null,
                                   atomicNumber int not null,
                                   atomicMass float not null,
                                   atomicGroup int not null,
                                   atomicPeriod int not null,
                                   electronegativity float
                               ); """
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create periodic table
        create_table(conn, sql_create_new_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
