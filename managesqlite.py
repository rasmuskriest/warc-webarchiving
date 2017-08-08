#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import shutil
import sqlite3
from pathlib import Path

def check_sqlite(dbname, database):
    """Check for SQLite database."""
    dbfile = Path(database)
    if dbfile.is_file():
        move_sqlite(dbname, database)
        return True
    else:
        return True

def move_sqlite(dbname, database):
    """Rename SQLite database with timestamp in case it already exists."""
    db_timestamp = datetime.fromtimestamp(Path.stat(database).st_mtime)
    shutil.move(database, (dbname, '_', db_timestamp, '.sqlite'))

def import_csv(csvfile, dbname):
    """Import CSV file to SQLite database."""
    database = (dbname, '.sqlite')
    table_name = 'warclist'  

    sqlite_exists = check_sqlite(dbname, database)

    if sqlite_exists:
        conn = sqlite3.connect(database)
        curs = conn.cursor()
        curs.execute("CREATE TABLE %s (id INTEGER PRIMARY KEY, Organization TEXT, Url TEXT, Last TEXT, State TEXT);", % (table_name))

        with open(csvfile,'rb') as readfile:
            readsite = csv.DictReader(readfile)

            to_db = [(i['Organization'], i['URL']) for i in readsite]


        curs.executemany("INSERT INTO %s (col1, col2) VALUES (?, ?);", to_db)
        conn.commit()
        conn.close()

def export_csv(csvfile, dbname):
    """Export SQLite database to CSV file."""
