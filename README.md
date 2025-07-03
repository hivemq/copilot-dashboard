# Copilot-dashboard

## Intro
GitHub only offers a 28-day retention period for Copilot metrics. This solution enables us to retrieve that data and visualize it using Metabase.

## Gh action
A GitHub Action retrieves the JSON metrics and renders them into a single JSON file. [Ref](*https://github.com/marketplace/actions/copilot-metrics-retention)

## Convert the json into SQlite dbfile
Open the terminal into the repo folder and run `python3 app.py`, visit the page `http://127.0.0.1:5000/`.
Load the `metrics.json`, click on `Convert & Download SQLite DB`, this will generate a .db file available under the upload folder having the name `copilot_metrics.db`

## Visualite the copilot_metrics.db via metabase

Download the `metabase.jar` [Link](https://downloads.metabase.com/v0.55.2/metabase.jar) and execute
```
java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar
```
This command will launch a Metabase server on port 3000 by default.

Access to it and complete the fake reistration, once in go to database and select `SQLite` and under path add `upload/copilot_metrics.db`, all data is available on the home page.

Enjoy!






