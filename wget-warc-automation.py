#!/usr/bin/python3

import csv
import subprocess

def archive_website(webarchivelist):
    with open(webarchivelist, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=csvdelimiter)
        for row in reader:
            subprocess.run(['./wget-warc.sh', row['URL']])

def append_csv(webarchivelist):
    with open(webarchivelist, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=csvdelimiter)
        writer.writerow({'done'})


if __name__ == "__main__":
    # Define webarchivelist to be the provided CSV with websites
    webarchivelist = './example.csv'
    csvheader = ['Organization','URL','Info1','Info2','Info3','Last','State']
    csvdelimiter = ','
    
    archive_website(webarchivelist)
    append_csv(webarchivelist)
                    