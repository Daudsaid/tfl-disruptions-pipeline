import psycopg2
from config import DB_CONFIG

def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tfl_disruptions (
            id SERIAL PRIMARY KEY,
            line_id VARCHAR(50),
            line_name VARCHAR(100),
            status VARCHAR(100),
            severity INTEGER,
            recorded_at TIMESTAMP WITH TIME ZONE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table ready")

def load(records):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    for record in records:
        cur.execute("""
            INSERT INTO tfl_disruptions 
            (line_id, line_name, status, severity, recorded_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            record["line_id"],
            record["line_name"],
            record["status"],
            record["severity"],
            record["recorded_at"]
        ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(records)} records")

if __name__ == "__main__":
    from extract import extract
    from transform import transform
    create_table()
    raw = extract()
    records = transform(raw)
    load(records)

    