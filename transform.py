from datetime import datetime, timezone

def transform(raw_data):
    records = []
    
    for line in raw_data:
        status = line["lineStatuses"][0]
        
        record = {
            "line_id": line["id"],
            "line_name": line["name"],
            "status": status["statusSeverityDescription"],
            "severity": status["statusSeverity"],
            "recorded_at": datetime.now(timezone.utc)
        }
        
        records.append(record)
    
    return records

if __name__ == "__main__":
    from extract import extract
    raw = extract()
    records = transform(raw)
    for r in records:
        print(r)