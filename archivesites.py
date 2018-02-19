#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to to the archiving based on a SQLite database and subprocess.run()"""

from datetime import datetime, date, time
import logging
import subprocess
import sqlite3

import managesqlite


def check_time():
    """Check whether websites should be archived."""
    now = datetime.now()
    # Change to time during which websites should be downloaded.
    if time(00, 00) <= now.time() <= time(23, 59):
        logging.info("check_time set True with now.time() == %s",
                     str(now.time()))
        return True

    # Fallback if passing midnight.
    elif time(00, 00) <= now.time() <= time(6, 00):
        logging.info("check_time set True with now.time() == %s",
                     str(now.time()))
        return True

    else:
        logging.info("check_time set False with now.time() == %s",
                     str(now.time()))
        return False


def write_state(conn, elem, import_sheet):
    """Write new state in respecting column of the database."""
    writecurs = conn.cursor()

    writecurs.execute('UPDATE {tn} SET {cl}=(?), {cs}=("done") WHERE {idf}=(?)'.
                      format(tn=import_sheet, cl="Last", cs="State", idf="Url"), (date.today(), elem))
    logging.info("%s successfully marked as done in %s", elem, import_sheet)


def download_site(download_dir, import_sheet, conn, elem):
    """Actually download the site with a subprocess."""
    logging.info("Downloading %s with subprocess.run() at %s",
                 elem, datetime.now())
    subprocess.run(['./wget.sh', elem, download_dir])
    write_state(conn, elem, import_sheet)
    logging.info("%s successfully downloaded with subprocess.run()", elem)


def archive_websites(download_dir, database, import_sheet, column_names):
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
            readcurs.execute('SELECT ({coi}) FROM {tn} WHERE {cn} IS NULL'.
                             format(coi="Url", tn=import_sheet, cn="State"))
            for row in readcurs:
                logging.info(readcurs)
                for elem in row:
                    download_site(download_dir, import_sheet, conn, elem)
            conn.commit()
            conn.close()

        # End of script when not in download time.
        else:
            logging.info("download_time == False")
            print("Archiving is not possible based on this machines current time (%s)."
                  % datetime.now())
            quit()

    # End of script when SQLite database does not exist.
    else:
        logging.info("sqlite_exists == False")
        print("Please create a database first.")
        quit()
