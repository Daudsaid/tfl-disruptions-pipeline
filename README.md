# TFL Live Disruptions Pipeline

A real-time data pipeline ingesting live TFL tube status data every 60 seconds.

## Pipeline Architecture
```
TFL API (every 60s) → Python ETL → PostgreSQL → dbt models → Snowflake/Databricks
```

## Tech Stack
- **Python** — extract, transform, load
- **PostgreSQL** — raw data storage
- **dbt** — staging, intermediate, mart models
- **Docker** — containerised pipeline
- **Snowflake/Databricks** — cloud analytics (coming soon)

## dbt Models
- `stg_tfl_disruptions` — staged raw data with severity categories
- `int_tfl_disruptions` — aggregated by hour
- `mart_line_status_summary` — line status summary table
- `mart_disruptions_by_hour` — disruptions trend by hour

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

## Data collected since: March 2026
