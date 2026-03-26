# TFL Live Disruptions Pipeline

A real-time data pipeline that ingests live TFL tube status data every 60 seconds, transforms it with dbt, and stores it in PostgreSQL for analysis.

## System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                          │
│         TFL API (api.tfl.gov.uk/line/mode/tube)         │
└─────────────────────────┬───────────────────────────────┘
                          │ Every 60 seconds
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  INGESTION LAYER                         │
│                                                          │
│   extract.py → transform.py → load.py                   │
│   (Python ETL running inside Docker container)           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   STORAGE LAYER                          │
│                                                          │
│         PostgreSQL (tfl_live_disruption_db)              │
│         Table: tfl_disruptions                           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               TRANSFORMATION LAYER (dbt)                 │
│                                                          │
│   staging/                                               │
│   └── stg_tfl_disruptions (view)                        │
│       └── cleaned + severity categories                  │
│                                                          │
│   intermediate/                                          │
│   └── int_tfl_disruptions (view)                        │
│       └── aggregated by hour                             │
│                                                          │
│   mart/                                                  │
│   ├── mart_line_status_summary (table)                   │
│   └── mart_disruptions_by_hour (table)                   │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               ANALYTICS LAYER (coming soon)              │
│                                                          │
│         Snowflake / Databricks                           │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python (requests, psycopg2, pandas) |
| Storage | PostgreSQL |
| Transformation | dbt |
| Containerisation | Docker |
| Cloud Analytics | Snowflake / Databricks (planned) |

## dbt Models

| Model | Type | Description |
|---|---|---|
| stg_tfl_disruptions | View | Cleaned raw data with severity categories |
| int_tfl_disruptions | View | Aggregated by hour |
| mart_line_status_summary | Table | Line status summary |
| mart_disruptions_by_hour | Table | Disruption trends by hour |

## Pipeline Flow
```
1. extract.py  — hits TFL API, returns raw JSON
2. transform.py — extracts line_id, name, status, severity, timestamp
3. load.py     — inserts records into PostgreSQL
4. main.py     — runs the loop every 60 seconds
```

## Running Locally
```bash
pip install -r requirements.txt
python3 main.py
```

## Running with Docker
```bash
docker build -t tfl-pipeline .
docker run -d --name tfl-pipeline \
  -e DB_HOST=host.docker.internal \
  -e DB_USER=daudsaid \
  -e DB_NAME=tfl_live_disruption_db \
  --restart always \
  tfl-pipeline
```

## dbt Commands
```bash
cd dbt/tfl_dbt
dbt run       # run all models
dbt test      # run all tests (11 tests)
dbt docs generate && dbt docs serve  # view DAG
```

## Data Collected

- **Started:** March 2026
- **Frequency:** Every 60 seconds
- **Lines tracked:** 11 tube lines
- **Records per hour:** ~660

## Author

Daud Abdi — github.com/Daudsaid
