#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
from configparser import ConfigParser
import logging
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
        help='run wget-warc or work with database'
        )
    parser.add_argument(
        '-c', '--config',
        action='store_true',
        help='custom path to user config file',
        default=(getcwd(), 'default.conf')
        )
    parser.add_argument(
        '-v', '--verbose',
        action='store_const', dest='loglevel', const=logging.INFO,
        help='enable verbose mode and get verbose info'
    )

    # Parse arguments.
    args = parser.parse_args()
    # Enable loglevel parsing.
    logging.basicConfig(level=args.loglevel)
    # Read config file, default.conf is set as default in parser.
    conf = ConfigParser()
    conf.read(args.config)
    download_dir = str(conf['Settings']['downloaddir'])
    csv_file = str(conf['Settings']['csvfile'])
    # Set db_name and database based on csv_file.
    db_name = str(path.splitext(path.basename(csv_file))[0])
    database = (db_name + '.sqlite')
    # Set table_name and columns manually.
    # TODO: Read column_names from csv_file with DictReader.
    table_name = 'warclist'
    column_names = ['Organization', 'Url', 'Last', 'State']
    column_url = 'Url'
    column_state = 'State'

    # Parse arguments and run accordingly.
    if args.mode == 'run':
        try:
            archivesites.archive_websites(download_dir, db_name, database, table_name, column_url, column_state)
        except Exception as exc:
            print(str(exc))
    elif args.mode == 'import':
        try:
            managesqlite.import_csv(csv_file, db_name, database, table_name, column_names)
        except Exception as exc:
            print(str(exc))
    elif args.mode == 'export':
        try:
            managesqlite.export_csv(csv_file, db_name, database, table_name)
        except Exception as exc:
            print(str(exc))
    else:
        parser.error("Unknown command")

if __name__ == "__main__":
    cli()
