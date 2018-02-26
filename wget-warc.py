#!/usr/bin/python3
# -*- coding: utf-8 -*-
""""Script to automate webarchiving with wget."""

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
        description='Script to automate webarchiving with wget.'
    )

    parser.add_argument(
        'mode',
        choices=['run', 'import', 'export'],
        help='run wget-warc or work with database'
    )
    parser.add_argument(
        '-c', '--config',
        metavar="FILE",
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
    excel_file = str(conf['Settings']['excelfile'])
    # Set db_name and database based on excel_file.
    db_name = str(path.splitext(path.basename(excel_file))[0])
    database = (db_name + '.sqlite')
    # Set worker number
    workers = int(conf['Settings']['workers'])
    # Set sheets for import / export and columns.
    import_sheet = 'import'
    export_sheet = 'export'
    column_names = ['Organization', 'Url',
                    'SizeWarc', 'SizeLog', 'Last', 'State']

    # Parse arguments and run accordingly.
    if args.mode == 'run':
        try:
            archivesites.archive_websites(
                download_dir,
                database,
                import_sheet,
                column_names,
                workers
            )
        except Exception as exc:
            print(str(exc))
    elif args.mode == 'import':
        try:
            managesqlite.import_excel(
                excel_file,
                db_name,
                database,
                import_sheet,
                column_names
            )
        except Exception as exc:
            print(str(exc))
    elif args.mode == 'export':
        try:
            managesqlite.export_excel(
                excel_file,
                database,
                export_sheet,
                column_names
            )
        except Exception as exc:
            print(str(exc))
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    cli()
