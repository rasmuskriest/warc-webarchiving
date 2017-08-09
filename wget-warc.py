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

    args = parser.parse_args()

    # Read config file, default.conf is set as default in parser.
    conf = ConfigParser()
    conf.sections()
    conf.read(args.config)
    downloaddir = conf['Settings']['downloaddir']
    csvfile = conf['Settings']['csvfile']
    dbname = str(path.splitext(path.basename(csvfile))[0])

    # Parse arguments and run accordingly.
    if args.mode == 'run':
        try:
            archivesites.archive_websites(downloaddir, csvfile, dbname)
        except Exception as e:
            print(str(e))
    elif args.mode == 'import':
        try:
            managesqlite.import_csv(csvfile, dbname)
        except Exception as e:
            print(str(e))
    elif args.mode == 'export':
        try:
            managesqlite.export_csv(csvfile, dbname)
        except Exception as e:
            print(str(e))
    else:
        parser.error("Unknown command")

if __name__ == "__main__":
    cli()
