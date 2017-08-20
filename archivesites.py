#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to to the archiving based on a SQLite database and subprocess.run()"""

from datetime import datetime, time
import logging
import subprocess
import sqlite3

import managesqlite

def check_time():
    """Check whether websites should be archived."""
    now = datetime.now()
    # Change to time during which websites should be downloaded.
    if time(00, 00) <= now.time() <= time(23, 59):
        logging.info("check_time set Truewith now.time() == %s", str(now.time()))
        return True

    # Fallback if passing midnight.
    elif time(00, 00) <= now.time() <= time(6, 00):
        logging.info("check_time set True with now.time() == %s", str(now.time()))
        return True

    else:
        logging.info("check_time set Falsewith now.time() == %s", str(now.time()))
        return False

def write_state(conn, row, sheet_name, column_url, column_state):
    """Write new state in respecting column of the database."""
    writecurs = conn.cursor()

    writecurs.execute('UPDATE {tn} SET {cn}=("done") WHERE {idf}=(?)'.\
        format(tn=sheet_name, cn=column_state, idf=column_url), row)
    logging.info("%s successfully marked as done in %s", (row, sheet_name))

#c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
#        format(tn=sheet_name, cn=column_name, idf=id_column))


def archive_websites(download_dir, db_name, database, sheet_name, column_url, column_state):
    """Archive websites from a csv"""
    sqlite_exists = managesqlite.check_sqlite(database)
    download_time = check_time()

    if sqlite_exists:
        logging.info("sqlite_exists == True")
        conn = sqlite3.connect(database)
        readcurs = conn.cursor()

        # Check for possible download time.
        if download_time is True:
            logging.info("download_time is True")
            # Select URL in rows that are not done
            readcurs.execute('SELECT ({coi}) FROM {tn} WHERE {cn}=""'.\
            format(coi=column_url, tn=sheet_name, cn=column_state))
            for row in readcurs:
                logging.info(readcurs)
                for elem in row:
                    logging.info("Downloading %s with subprocess.run()", elem)
                    subprocess.run(['./wget.sh', elem, download_dir])
                    write_state(conn, row, sheet_name, column_url, column_state)
                    logging.info("%s successfully downloaded with subprocess.run()", elem)
            conn.commit()
            conn.close()

        # End of script when not in download time.
        else:
            logging.info("download_time == False")
            print("Archiving is not possible based on this machines current time (%s)."\
            % datetime.now())
            quit()

    # End of script when SQLite database does not exist.
    else:
        logging.info("sqlite_exists == False")
        print("Please create a database first.")
        quit()
