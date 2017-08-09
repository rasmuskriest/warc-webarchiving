#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import shutil
import sqlite3
from os.path import getmtime
from pathlib import Path

def check_sqlite(dbname, database):
    """Check for SQLite database."""
    dbfile = Path(database)
    if dbfile.is_file():
        move_sqlite(dbname, database)
        return True
        #print("check_sqlite moved the old database and set True")
    else:
        return True
        #print("check_sqlite set True")

def move_sqlite(dbname, database):
    """Rename SQLite database with timestamp in case it already exists."""
    db_timestamp = str(datetime.fromtimestamp(getmtime(database)).strftime('%Y-%m-%d_%H-%M-%S'))
    shutil.move(database, (dbname + '_' + db_timestamp + '.sqlite'))

def import_csv(csvfile, dbname):
    """Import CSV file to SQLite database."""
    database = (dbname + '.sqlite')
    table_name = 'warclist'
    column_names = ['Organization', 'Url', 'Last', 'State']
    # TODO: Read column_names from csvfile with DictReader.

    sqlite_exists = check_sqlite(dbname, database)

    # True is the only possible case.
    if sqlite_exists:
        conn = sqlite3.connect(database)
        curs = conn.cursor()
        # Create table based on column_names
        curs.execute("CREATE TABLE {} (Id INTEGER PRIMARY KEY, {} TEXT, {} TEXT, {} TEXT, {} TEXT);".format(table_name, (*column_names)))

        # Import csvfile into database
        with open(csvfile,'r') as readfile:
            readsite = csv.DictReader(readfile)
            for row in readsite:
                to_db = list()
                for column in column_names:
                    to_db.append(row[column])
                #print(to_db)
                curs.execute("INSERT INTO {} ({}, {}, {}, {}) VALUES (?, ?, ?, ?);".format(table_name, (*column_names)), to_db)
                
        conn.commit()
        conn.close()

def export_csv(csvfile, dbname):
    """Export SQLite database to CSV file."""
