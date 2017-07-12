#!/usr/bin/python3

import csv
import subprocess

# Define webarchivelist to be the provided CSV with websites
webarchivelist = './example.csv'

with open(webarchivelist) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        subprocess.run(['./wget-warc.sh', row['URL']])
        