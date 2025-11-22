# This is a markdown file for the `monitoring.py` script that is written inside the pentesting practice to Andromeda.

## Core Features
- Real-time Monitoring: Continuously checks server availability.
- Latency Measurement: Precisely measures connection response times in milliseconds.
- Connection Testing: Validates TCP connectivity to specified port.
- Timestamped Logging: Each check includes precise datetime stamps

## Technical Capabilities
- Configurable Target: Easy modification of IP and port.
- Adjustable Intervals: Customizable check frequency (2 seconds default).
- Timeout Handling: Configurable connection timeout (3 seconds default).
- Error Reporting: Detailed failure messages with specific socket errors.

## Output Example
```bash
[+] Starting passive monitor on <IP_ADDRESS>
[2024-01-15 14:30:01.123456]  SUCCESS - Latency: 15.42 ms
[2024-01-15 14:30:03.125678]  FAIL - [Errno 111] Connection refused
[2024-01-15 14:30:05.127890]  SUCCESS - Latency: 18.75 ms
```

# NOTE: This is a legitimate monitoring tool, not an attack script. It performs simple connectivity checks without overwhelming the target.
