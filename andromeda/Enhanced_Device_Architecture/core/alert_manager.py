from datetime import datetime
import os

LOG_FILE = "alerts.log"

def log_alert(msg, level="warning"):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} [{level.upper()}] {msg}\n")

def get_alerts():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE) as f:
        return [line.strip() for line in f.readlines()]