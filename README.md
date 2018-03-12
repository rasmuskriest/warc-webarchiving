Skripte zur automatisierten Webarchivierung mithilfe von `wget` oder `wpull`.

Zur Erläuterung der verschiedenen Argumente ist das [GNU Wget Manual](https://www.gnu.org/software/wget/manual/wget.html) oder das [GitHub-Repository von `wpull`](https://github.com/chfoo/wpull) heranzuziehen.

## Nutzung

Die automatisierte Webarchivierung kann mit dem Parameter `run` angestoßen werden. Hierbei werden als Verzeichnis für den Download das in der `default.conf` genannte `downloaddir` verwendet:

```
python warc-webarchiving.py run
```

Zuvor muss allerdings eine Excel-Datei (in der `default.conf` per `excelfile` definiert) importiert werden. Auch der Export ist möglich:

```
python warc-webarchiving.py import
python warc-webarchiving.py export
```

Der Befehl `-h` zeigt alle Optionen auf:

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

## Voraussetzungen

`warc-webarchiving` funktioniert nur mit einer `venv` innerhalb von _Python 3_ (aktuell mind. 3.5); die benötigten externen Module lassen sich mit dem Befehl `pip install -r requirements.txt` installieren.

## To-Do / Missings

* Der Umgang mit Fehlermeldungen fehlt (fast) vollständig.
* Die Namen der Überschriften aus der Excel-Tabelle sind aktuell hardcoded.
