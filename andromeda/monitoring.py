import socket
import time
from datetime import datetime

# Easy modifiable parameters
target = "192.168.2.8"
port = 80
check_interval = 2  # seconds
timeout = 3         # connection timeout

def check_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        start = time.time()
        s.connect((target, port))
        end = time.time()
        s.close()
        latency = round((end - start) * 1000, 2)
        return f"[{datetime.now()}]  SUCCESS - Latency: {latency} ms"
    except socket.error as e:
        return f"[{datetime.now()}]  FAIL - {e}"

print(f"[+] Starting passive monitor on {target}:{port}")
while True:
    result = check_server()
    print(result)
    time.sleep(check_interval)
