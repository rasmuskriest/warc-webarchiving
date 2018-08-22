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

## Usage with Docker

This project can be run indepently of local Python versions by using [_Docker_](https://www.docker.com/) and [_Docker Compose_](https://docs.docker.com/compose/). Both `import` and `run` are executed when started with `docker-compose up --build`.

**Configuration is a bit patchy when using _Docker_ as of now.** Inside the respective `.conf`, both `downloaddir = ./WARC` as well as `excelfile = ./config/` must not be changed - the specific _Excel_ file has to be named though. Instead, most configuration is handled by _Docker's_ `.env` file: `DOWNLOAD_VOLUME` is mapped into `downloaddir` inside the `.conf`. Also, the arguments `--config` and `--engine` are handled by _Docker_.

## License

Copyright (c) 2018 Rasmus Kriest
The code in this project is licensed under MIT license.
