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
usage: wget-warc [-h] [-c] [-v] {run,import,export}

Scripts to automate webarchiving with wget.

positional arguments:
  {run,import,export}  run wget-warc or work with database.

optional arguments:
  -h, --help           show this help message and exit
  -c, --config         custom path to user config file
  -v, --verbose        enable verbose mode and get verbose info
```

## Voraussetzungen

`wget-warc` funktioniert nur mit einer `venv` innerhalb von _Python 3_ (aktuell mind. 3.5); die benötigten externen Module lassen sich mit dem Befehl `pip install -r requirements.txt` installieren.

## To-Do / Missings

* Webseiten, deren URL entweder kyrillische Buchstaben aufweist oder `/` enthält, lassen sich derzeit nicht herunterladen. Sie sollten daher vor dem Import ausgeschlossen werden.
* Der Umgang mit Fehlermeldungen fehlt (fast) vollständig. Daher wird `State == done`, obwohl der Download fehlschlägt.
* Der Export von der SQLite in eine CSV-Datei ist noch nicht implementiert.
* Die Funktion `check_time()` wird zwar aufgerufen, hat allerdings keine Auswirkungen.
* Die Namen der Überschriften aus dem CSV-Datensatz sind aktuell hardcoded.
