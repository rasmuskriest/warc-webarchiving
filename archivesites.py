#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to to the archiving based on a SQLite database and subprocess.run()"""

from datetime import datetime, date, time
import logging
import multiprocessing
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


def write_state(database, elem, import_sheet):
    """Write new state in respecting column of the database."""
    conn = sqlite3.connect(database)
    writecurs = conn.cursor()

    writecurs.execute('UPDATE {tn} SET {cl}=(?), {cs}=("done") WHERE {idf}=(?)'.
                      format(tn=import_sheet, cl="Last", cs="State", idf="Url"), (date.today(), elem))
    logging.info("%s successfully marked as done in %s", elem, import_sheet)

    conn.commit()
    conn.close()


def download_site(download_dir, import_sheet, database, elem):
    """Actually download the site with a subprocess."""
    logging.info("Downloading %s with subprocess.run() at %s",
                 elem, datetime.now())
    subprocess.run(['./wget.sh', elem, download_dir], cwd='./wget')
    logging.info(
        "%s successfully downloaded with subprocess.run() at %s", elem, datetime.now())
    write_state(database, elem, import_sheet)


def work_sqlite(num, database, import_sheet, download_dir, column_names, workers):
    """Work in SQLite database to find URLs to download."""
    logging.info("Worker %s of %s", num, int(workers - 1))
    conn = sqlite3.connect(database)
    readcurs = conn.cursor()
    # Select URL in rows that are not done
    readcurs.execute('SELECT ({coi}) FROM {tn} WHERE {cn} IS NULL'.
                     format(coi="Url", tn=import_sheet, cn="State"))

    sites = readcurs.fetchall()
    logging.info(sites)
    # Close database immediately after fetching entry.
    conn.close()

    # Get specific rows based on worker number
    rows = sites[num::workers]
    logging.info("Worker %s will download %s", num, rows)
    for row in rows:
        for elem in row:
            download_site(download_dir, import_sheet, database, elem)


def archive_websites(download_dir, database, import_sheet, column_names, workers):
    """Archive websites from a csv"""
    sqlite_exists = managesqlite.check_sqlite(database)
    download_time = check_time()

    if sqlite_exists:
        logging.info("sqlite_exists == True")

        # Check for possible download time.
        if download_time is True:
            logging.info("download_time is True")

            # Start multiprocessing
            jobs = []
            # Define number of workers
            for num in range(workers):
                p = multiprocessing.Process(target=work_sqlite, args=(
                    num, database, import_sheet, download_dir, column_names, workers))
                jobs.append(p)
                p.start()

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
