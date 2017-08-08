#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime, time
from pathlib import Path
import subprocess
import time as waittime

# Define global variables realted to the CSV.
WARC_LIST = './example.csv'
CSV_DELIMITER = ','

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

def check_sqlite():
    """Check for SQLite database."""
    dbfile = Path("sitedb.sqlite")
    if dbfile.is_file():
        return True
        #print("check_sqlite set True")
        
    else:
        return False
        #print("check_sqlite set False")

def archive_websites():
    """Archive websites from a csv"""
    download_time = check_time()

    with open(WARC_LIST, 'r') as readfile:
        readsite = csv.DictReader(readfile, delimiter=CSV_DELIMITER)

        for row in readsite:
            #waittime.sleep(5)
            
            # Check for possible download time.
            if download_time is True:
                print("It is time to download!")
                
                # Check whether site has not been downloaded.
                if row['State'] == "":
                    print("Downloading", row['Organization'], "|", row['URL'])
                    subprocess.run(['./wget-warc.sh', row['URL']])
                    print(row['Organization'], "|", row['URL'], "successfully downloaded.")
                    download_status = True
                    #append_csv(download_status)
                
                # Skip to next row if site has been downloaded.
                elif row['State'] == "done":
                    print(row['Organization'], "|", row['URL'], "is already downloaded.")
                    download_status = False
                    #append_csv(download_status)
                    next(readsite)
                   
                # Fallback in case of manual edits.
                else:
                    print(
                        "An error occured when trying to download",
                        row['Organization'],
                        "|",
                        row['URL']
                        )
                    download_status = False
                    #append_csv(download_status)
                    next(readsite)
            
            # End of script when not in download time.
            else:
                print("Cannot download right now.")
                quit()
