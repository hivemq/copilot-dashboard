# Copilot-dashboard

## Intro
Unfortunately Github only offers 28-day retention for the copilot metrics, this solution gives us the ability to retrieve data and visulasie them via metabase.

## Gh action
There is a gh action that retrieves the json file and render it into a unique json. [Ref](*https://github.com/marketplace/actions/copilot-metrics-retention)

## Convert the json into SQlite dbfile
Open the terminal into the repo folder and run `python3 app.py`, visit the page `http://127.0.0.1:5000/`, download the json artifact and load the file, click on `Convert & Download SQLite DB`, this will generate a .db file available under the upload folder having the name `copilot_metrics.db`

## Visualite the copilot_metrics.db via metabase

Download the `metabase.jar` [Link](https://downloads.metabase.com/v0.55.2/metabase.jar) and execute
```
java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar
```
This command will launch a Metabase server on port 3000 by default.

Access to it and complete the fake reistration, once in go to database and select `SQLite` and under path add `upload/copilot_metrics.db`, all data is available on the home page.

Enjoy!






