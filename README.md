# TFL Disruptions Pipeline

A real-time serverless data pipeline that polls the TFL API every 60 seconds and stores tube line disruption data on AWS.

## Architecture
```
EventBridge (every 60s)
    → Step Functions
        → Lambda (polls TFL API → writes NDJSON to S3)
        → Glue (transforms JSON → Parquet)
    → Athena (SQL queries on processed data)
```

## AWS Services Used

- **EventBridge Scheduler** — triggers the pipeline every 60 seconds
- **Step Functions** — orchestrates Lambda and Glue with retry and error handling
- **Lambda** — polls the TFL API and writes raw NDJSON to S3
- **S3** — stores raw JSON (`tfl-disruptions-raw`) and processed Parquet (`tfl-disruptions-processed`)
- **Glue** — transforms NDJSON to Parquet partitioned by `line_id`
- **Athena** — SQL interface over the processed Parquet data

## Project Structure
```
tfl-disruptions-pipeline/
├── lambda/
│   ├── lambda_function.py   # Polls TFL API, writes NDJSON to S3
│   └── requirements.txt
├── glue/
│   └── glue_job.py          # Transforms JSON to Parquet
├── step_functions/
│   └── state_machine.json   # Step Functions definition
├── infra/
├── dbt/
│   └── tfl_dbt/             # dbt models for Athena
└── README.md
```

## Data Flow

1. EventBridge fires every 60 seconds
2. Step Functions starts execution
3. Lambda polls `https://api.tfl.gov.uk/line/mode/tube/status`
4. Raw NDJSON written to `s3://tfl-disruptions-raw/raw/YYYY/MM/DD/HH-MM-SS.json`
5. Glue transforms to Parquet partitioned by `line_id`
6. Parquet written to `s3://tfl-disruptions-processed/processed/line_id=*/`
7. Athena queries via `tfl_aws.tfl_disruptions` table

## dbt Models

| Model | Type | Description |
|---|---|---|
| `stg_tfl_disruptions` | view | Staged data with severity categories |
| `int_tfl_disruptions` | view | Hourly aggregations per line |
| `mart_disruptions_by_hour` | table | Disrupted vs total lines per hour |
| `mart_line_severity` | table | Severity summary per line |

## Sample Athena Query
```sql
SELECT line_id, status, severity, recorded_at
FROM tfl_aws.tfl_disruptions
WHERE line_id = 'northern'
ORDER BY recorded_at DESC
LIMIT 10;
```

## Tech Stack

- Python 3.13
- AWS Lambda, Glue, Athena, S3, Step Functions, EventBridge
- Apache Spark (via AWS Glue)
- dbt
- Parquet / Snappy compression
