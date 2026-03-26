import time
from extract import extract
from transform import transform
from load import load, create_table
from config import POLL_INTERVAL_SECONDS

def run():
    print("TFL Disruptions Pipeline started...")
    create_table()
    
    while True:
        try:
            print(f"Fetching TFL data...")
            raw = extract()
            records = transform(raw)
            load(records)
            print(f"Sleeping {POLL_INTERVAL_SECONDS} seconds...\n")
            time.sleep(POLL_INTERVAL_SECONDS)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run()