# core/monitor_thread.py
import threading
import time
import psutil
import subprocess
from core.alert_bot import send_telegram_alert
from core.power_monitor import get_power_data

CPU_THRESHOLD = 85
POWER_THRESHOLD = 70
PING_TARGET = "8.8.8.8"

def ping(host):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "2", host])
        return True
    except subprocess.CalledProcessError:
        return False

def monitor_loop():
    while True:
        try:
            cpu = psutil.cpu_percent()
            if cpu > CPU_THRESHOLD:
                send_telegram_alert(f"CPU usage high: {cpu:.1f}% 🔥", "warning")

            power = get_power_data().get("power", 0)
            if power > POWER_THRESHOLD:
                send_telegram_alert(f"Power consumption high: {power}W ⚡", "warning")

            if not ping(PING_TARGET):
                send_telegram_alert(f"Network connection lost to {PING_TARGET} ❌", "error")

        except Exception as e:
            print("Monitor error:", e)

        time.sleep(60)  # check every minute

def start_monitor():
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()
