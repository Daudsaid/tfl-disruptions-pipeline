import json
import boto3
import requests
from datetime import datetime, timezone

TFL_API_URL = "https://api.tfl.gov.uk/line/mode/tube/status"
S3_BUCKET = "tfl-disruptions-raw"

s3 = boto3.client("s3")

def extract():
    response = requests.get(TFL_API_URL)
    response.raise_for_status()
    return response.json()

def transform(raw_data):
    records = []
    for line in raw_data:
        status = line["lineStatuses"][0]
        records.append({
            "line_id": line["id"],
            "line_name": line["name"],
            "status": status["statusSeverityDescription"],
            "severity": status["statusSeverity"],
            "recorded_at": datetime.now(timezone.utc).isoformat()
        })
    return records

def handler(event, context):
    print("Lambda triggered — fetching TFL data...")

    raw = extract()
    records = transform(raw)

    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H-%M-%S")
    key = f"raw/{timestamp}.json"

    ndjson = "\n".join(json.dumps(r) for r in records)

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=ndjson,
        ContentType="application/json"
    )

    print(f"Written {len(records)} records to s3://{S3_BUCKET}/{key}")

    return {
        "statusCode": 200,
        "records_written": len(records),
        "s3_key": key
    }
