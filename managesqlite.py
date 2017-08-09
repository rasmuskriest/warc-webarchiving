#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import shutil
import sqlite3
from os.path import getmtime
from pathlib import Path

def check_sqlite(db_name, database):
    """Check for SQLite database."""
    dbfile = Path(database)
    if dbfile.is_file():
        move_sqlite(db_name, database)
        return True
        #print("check_sqlite moved the old database and set True")
    else:
        return True
        #print("check_sqlite set True")

def move_sqlite(db_name, database):
    """Rename SQLite database with timestamp in case it already exists."""
    db_timestamp = str(datetime.fromtimestamp(getmtime(database)).strftime('%Y-%m-%d_%H-%M-%S'))
    shutil.move(database, (db_name + '_' + db_timestamp + '.sqlite'))

def import_csv(csv_file, db_name, database, table_name, column_names):
    """Import CSV file to SQLite database."""
    sqlite_exists = check_sqlite(db_name, database)

    # True is the only possible case.
    if sqlite_exists:
        conn = sqlite3.connect(database)
        curs = conn.cursor()
        # Create table based on column_names
        curs.execute("CREATE TABLE {} (Id INTEGER PRIMARY KEY, {} TEXT, {} TEXT, {} TEXT, {} TEXT);".\
        format(table_name, (*column_names)))

        # Import csv_file into database
        with open(csv_file,'r') as readfile:
            readsite = csv.DictReader(readfile)
            for row in readsite:
                to_db = list()
                for column in column_names:
                    to_db.append(row[column])
                #print(to_db)
                curs.execute("INSERT INTO {} ({}, {}, {}, {}) VALUES (?, ?, ?, ?);".\
                format(table_name, (*column_names)), to_db)
                
        conn.commit()
        conn.close()

def export_csv(csv_file, db_name, database, table_name):
    """Export SQLite database to CSV file."""
