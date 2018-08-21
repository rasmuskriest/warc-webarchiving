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
        prog='warc-webarchiving',
        description='Script to automate webarchiving with wget.'
    )

    parser.add_argument(
        'mode',
        choices=['run', 'import', 'export'],
        help='run warc-webarchiving or work with database'
    )
    parser.add_argument(
        '--engine',
        choices=['wget', 'wpull'],
        help='choose engine for archving (default: wget)',
        default='wget'
    )
    parser.add_argument(
        '-c', '--config',
        metavar="FILE",
        help='custom path to user config file (default: ./config/default.conf)',
        default=(getcwd(), 'config/default.conf')
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_const', dest='loglevel', const=logging.INFO,
        help='enable verbose mode and get verbose info'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_const', dest='loglevel', const=logging.DEBUG,
        help='enable debug mode and get debug info'
    )

    # Create dictionary 'dataset'
    dataset = dict()

    # Parse arguments.
    args = parser.parse_args()

    # Read config file, default.conf is set as default in parser.
    conf = ConfigParser()
    conf.read(args.config)

    # Set download_dir and worker number from config.
    download_dir = str(path.abspath(conf['Settings']['downloaddir']))
    workers = int(conf['Settings']['workers'])

    dataset['excel_file'] = str(conf['Settings']['excelfile'])

    # Set db_name and database based on excel_file.
    dataset['db_name'] = str(path.splitext(
        path.basename(dataset['excel_file']))[0])
    dataset['db_path'] = str(path.split(dataset['excel_file'])[0] + '/')
    dataset['database'] = (dataset['db_path'] + dataset['db_name'] + '.sqlite')

    # Set sheets for import / export and columns.
    dataset['import_sheet'] = 'import'
    dataset['export_sheet'] = 'export'
    dataset['column_names'] = ['Organization', 'Url',
                               'Folder', 'SizeWarc', 'SizeLog', 'DownloadDelta', 'Last', 'State']

    # Enable loglevel parsing.
    logging.basicConfig(level=args.loglevel,
                        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
                        handlers=[
                            logging.FileHandler(
                                "{0}/{1}.log".format(dataset['db_path'], dataset['db_name'])),
                            logging.StreamHandler()
                        ]
                        )
    # Set engine to use for archiving / download
    engine = args.engine

    # Parse arguments and run accordingly.
    if args.mode == 'run':
        try:
            archivesites.archive_websites(
                download_dir,
                dataset,
                workers,
                engine
            )
        except Exception as exc:
            print(str(exc))
    elif args.mode == 'import':
        try:
            managesqlite.import_excel(
                dataset
            )
        except Exception as exc:
            print(str(exc))
    elif args.mode == 'export':
        try:
            managesqlite.export_excel(
                dataset
            )
        except Exception as exc:
            print(str(exc))
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    cli()
