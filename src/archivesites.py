#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to to the archiving based on a SQLite database and subprocess.run()"""

from datetime import datetime, date, time
import logging
import multiprocessing
from os.path import getsize
import subprocess
import sqlite3
from pathlib import Path

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


def write_state(database, url, folder, import_sheet, download_dir, diff_time):
    """Write new state in respecting column of the database."""
    conn = sqlite3.connect(database)
    writecurs = conn.cursor()

    warcpath = (download_dir + '/' + folder + '.warc.gz')
    logpath = (download_dir + '/' + folder + '.log')

    if warcpath.is_file():
        size_warc = float(getsize(download_dir + '/' +
                                  folder + '.warc.gz') / float(1 << 20))
        logging.debug("WARC size: %s", size_warc)
    else:
        size_warc = 'NULL'

    if logpath.is_file():
        size_log = float(getsize(download_dir + '/' +
                                 folder + '.log') / float(1 << 20))
        logging.debug("Log size: %s", size_log)
    else:
        size_log = 'NULL'

    writecurs.execute('UPDATE {tn} SET {csw}=(?), {csl}=(?), {cst}=(?), {cl}=(?), {cs}=("done") WHERE {idf}=(?)'.
                      format(tn=import_sheet, csw="SizeWarc", csl="SizeLog", cst="DownloadDelta", cl="Last", cs="State", idf="Url"), (size_warc, size_log, diff_time, date.today(), url))
    logging.info("%s successfully marked as done in %s", url, import_sheet)

    conn.commit()
    conn.close()


def download_site(download_dir, import_sheet, database, url, folder, engine, default_engine):
    """Actually download the site with a subprocess."""

    if engine != None:
        logging.debug("Using engine: %s", engine)

        start_time = datetime.now()
        logging.info("Downloading %s with subprocess.run() at %s with %s",
                     url, start_time, engine)

        if engine == 'httrack':
            subprocess.run(['./httrack.sh', url, folder,
                            download_dir], cwd='./httrack')

        if engine == 'wget':
            subprocess.run(['./wget.sh', url, folder,
                            download_dir], cwd='./wget')

        if engine == 'wpull':
            subprocess.run(['./wpull.sh', url, folder,
                            download_dir], cwd='./wpull')

    else:
        logging.debug("Using default engine: %s", default_engine)

        start_time = datetime.now()
        logging.info("Downloading %s with subprocess.run() at %s with %s",
                     url, start_time, default_engine)

        if default_engine == 'httrack':
            subprocess.run(['./httrack.sh', url, folder,
                            download_dir], cwd='./httrack')

        if default_engine == 'wget':
            subprocess.run(['./wget.sh', url, folder,
                            download_dir], cwd='./wget')

        if default_engine == 'wpull':
            subprocess.run(['./wpull.sh', url, folder,
                            download_dir], cwd='./wpull')

    end_time = datetime.now()
    diff_time = str(end_time - start_time)
    logging.info(
        "%s successfully downloaded with subprocess.run() at %s, that took %s", url, end_time, diff_time)

    # If httrack is being used as engine, an automatic conversion to WARC is tried. It will fail in case Java is not installed on the machine.
    if engine == 'httrack':
        logging.info("Converting %s to WARC", url)
        subprocess.run(['./convert2warc.sh', folder,
                        download_dir], cwd='./httrack')
        logging.info("%s successfully converted", url)

    write_state(database, url, folder, import_sheet,
                download_dir, diff_time)


def work_sqlite(num, database, import_sheet, download_dir, column_names, workers, default_engine):
    """Work in SQLite database to find URLs to download."""
    logging.info("Worker %s of %s", num, int(workers - 1))
    conn = sqlite3.connect(database)
    readcurs = conn.cursor()
    # Select URL in rows that are not done
    readcurs.execute('SELECT ({coi}), ({coj}), ({cok}) FROM {tn} WHERE {cn} IS NULL'.
                     format(coi="Url", coj="Folder", cok="Engine", tn=import_sheet, cn="State"))

    sites = readcurs.fetchall()
    logging.debug(sites)
    # Close database immediately after fetching entry.
    conn.close()

    # Get specific rows based on worker number
    rows = sites[num::workers]
    logging.debug("Worker %s got dict %s", num, rows)
    logging.info("Worker %s will download %s", num, rows)
    for row in rows:
        url = row[0]
        folder = row[1]
        engine = row[2]
        logging.debug("url = %s, folder = %s, engine = %s",
                      url, folder, engine)
        download_site(download_dir, import_sheet,
                      database, url, folder, engine, default_engine)


def archive_websites(download_dir, dataset, workers, default_engine):
    """Archive websites from a csv"""
    sqlite_exists = managesqlite.check_sqlite(dataset['database'])
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
                    num, dataset['database'], dataset['import_sheet'], download_dir, dataset['column_names'], workers, default_engine))
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
