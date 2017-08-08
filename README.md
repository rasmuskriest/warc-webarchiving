Skripte zur automatisierten Webarchivierung mithilfe von `wget`.

Zur Erläuterung der verschiedenen Argumente ist das [GNU Wget Manual](https://www.gnu.org/software/wget/manual/wget.html) heranzuziehen.

## Nutzung

Die automatisierte Webarchivierung kann mit dem Parameter `run` angestoßen werden. Hierbei werden als Verzeichnis für den Download das in der `default.conf` genannte `downloaddir` und als Liste das `csvfile` verwendet:

```
python wget-warc.py run
```

Für einen manuellen Im- oder Export zwischen CSV-Liste und SQLite-Datenbank 

```
python wget-warc.py import
python wget-warc.py export
```

Der Befehl `-h` zeigt alle Optionen auf:

```
usage: wget-warc [-h] [-c] {run,import,export}

Scripts to automate webarchiving with wget.

positional arguments:
  {run,import,export}  run wget-warc or work with database.

optional arguments:
  -h, --help           show this help message and exit
  -c, --config         custom path to user config file
```

## Requirements 

`wget-warc` funktioniert am besten in einer `venv` unter _Python 3_.
