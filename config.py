import os

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root1234"),
    "database": os.getenv("DB_NAME", "ims_db"),
}

THRESHOLDS = {
    "temperature": {"min": 10,  "max": 80},   # °C
    "pressure":    {"min": 1.0, "max": 10.0}, # bar
    "flow_rate":   {"min": 5,   "max": 50},   # L/min
}