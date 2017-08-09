#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime, time
import subprocess
import sqlite3

import managesqlite

def check_time():
    """Check whether websites should be archived."""
    now = datetime.now()
    # Change to time during which websites should be downloaded.
    if time(00, 00) <= now.time() <= time(23, 59):
        return True
        #print("check_time set True")

    # Fallback if passing midnight.
    elif time(00, 00) <= now.time() <= time(6, 00):
        return True
        #print("check_time set True")

    else:
        return False
        #Print("check_time set False")

def write_state(conn, row, table_name, column_url, column_state):
    """Write new state in respecting column of the database."""
    writecurs = conn.cursor()

    writecurs.execute('UPDATE {tn} SET {cn}=("done") WHERE {idf}=(?)'.\
        format(tn=table_name, cn=column_state, idf=column_url), row)
    #print(row, "successfully marked as done.")

#c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
#        format(tn=table_name, cn=column_name, idf=id_column))


def archive_websites(download_dir, db_name, database, table_name, column_url, column_state):
    """Archive websites from a csv"""
    #sqlite_exists = managesqlite.check_sqlite(db_name, database)
    sqlite_exists = True #TODO: Check for database and act accordingly.
    download_time = check_time()

    if sqlite_exists: 
        conn = sqlite3.connect(database)
        readcurs = conn.cursor()

        # Check for possible download time.
        if download_time is True:
            #print("It is time to download!")
            # Select URL in rows that are not done
            readcurs.execute('SELECT ({coi}) FROM {tn} WHERE {cn}=""'.\
            format(coi=column_url, tn=table_name, cn=column_state))
            for row in readcurs:
                #print(curs)
                for elem in row:
                    #print("Downloading", elem)
                    subprocess.run(['./wget.sh', elem, download_dir])
                    # TODO: Give download_dir to script.
                    write_state(conn, row, table_name, column_url, column_state)
                    #print(elem, "successfully downloaded.")
            conn.commit()
            conn.close()

        # End of script when not in download time.
        else:
            print("Cannot download right now.")
            quit()
