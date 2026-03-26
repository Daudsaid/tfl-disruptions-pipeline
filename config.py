import os

# TFL API
TFL_API_URL = "https://api.tfl.gov.uk/line/mode/tube/status"

# PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "tfl_live_disruption_db"),
    "user": os.getenv("DB_USER", "daudsaid"),
    "password": os.getenv("DB_PASSWORD", "")
}

# Pipeline settings
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 60))
