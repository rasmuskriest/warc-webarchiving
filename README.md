Python script to automate webarchiving with `wget` or `wpull`.

## Installation

Clone the repository, create a virtual enviroment (currently Python 3.5+), do `pip install -r requirements.txt`.

## Usage

`warc-webarchiving.py` is the main script, `config\default.conf` the default configuration file, `config\example.xlsx` the default table.

```
usage: warc-webarchiving [-h] [--engine {wget,wpull}] [-c FILE] [-v] [-d]
                         {run,import,export}

Script to automate webarchiving with wget.

positional arguments:
  {run,import,export}   run warc-webarchiving or work with database

optional arguments:
  -h, --help            show this help message and exit
  --engine {wget,wpull}
                        choose engine for archving (default: wget)
  -c FILE, --config FILE
                        custom path to user config file (default:
                        ./config/default.conf)
  -v, --verbose         enable verbose mode and get verbose info
  -d, --debug           enable debug mode and get debug info
```

### Example

In this example, the table `example.xlsx` (referred to in `default.conf`) is being imported and a download with the default engine (`wpull`) is started. Afterwards, the SQLite database is written into another sheet inside `example.xlsx`.

```
python warc-webarchiving.py import
python warc-webarchiving.py run
python warc-webarchiving.py export
```

## License

Copyright (c) 2018 Rasmus Kriest
The code in this project is licensed under MIT license.
