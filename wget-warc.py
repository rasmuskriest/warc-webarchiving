#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
from configparser import ConfigParser
from itertools import chain
from os import getcwd, path

import archivesites
import managesqlite

def cli():
    """Main CLI interface"""

    # Add argument parser. Possible commands can be shown with -h parameter.
    parser = argparse.ArgumentParser(
        prog='wget-warc',
        description='Scripts to automate webarchiving with wget.'
        )

    parser.add_argument(
        'mode',
        choices=['run', 'import', 'export'],
        help='run wget-warc or work with database.'
        )
    parser.add_argument(
        '-c', '--config',
        action='store_true',
        help='custom path to user config file',
        default=(getcwd(), 'default.conf'))
    #TODO: Add -v / --verbose mode and change all prints accordingly.

    args = parser.parse_args()

    # Read config file, default.conf is set as default in parser.
    conf = ConfigParser()
    conf.sections()
    conf.read(args.config)
    download_dir = conf['Settings']['downloaddir']
    csv_file = conf['Settings']['csvfile']
    db_name = str(path.splitext(path.basename(csv_file))[0])
    database = (db_name + '.sqlite')
    table_name = 'warclist'

    # Parse arguments and run accordingly.
    if args.mode == 'run':
        try:
            archivesites.archive_websites(download_dir, csv_file, db_name, database, table_name)
        except Exception as e:
            print(str(e))
    elif args.mode == 'import':
        try:
            managesqlite.import_csv(csv_file, db_name, database, table_name)
        except Exception as e:
            print(str(e))
    elif args.mode == 'export':
        try:
            managesqlite.export_csv(csv_file, db_name, database, table_name)
        except Exception as e:
            print(str(e))
    else:
        parser.error("Unknown command")

if __name__ == "__main__":
    cli()
