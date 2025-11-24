#!/bin/bash
TARGET="192.168.2.8"

echo "COMPREHENSIVE REMOTE ASSESSMENT"

# 1. Network mapping
echo "1. Network mapping..."
nmap -sS -sV -sC -O $TARGET > network_scan.txt

# 2. Service enumeration
echo "2. Service enumeration..."
nmap -p- --open $TARGET > open_ports.txt

# 3. Vulnerability scanning
echo "3. Vulnerability detection..."
nmap --script vuln $TARGET > vulnerabilities.txt

# 4. Web application testing (if port 80/443 open)
echo "4. Web application testing..."
nikto -h http://$TARGET > web_scan.txt

# 5. Internal audit (requires credentials)
echo "5. Internal configuration audit..."
ssh andromeda@$TARGET "sudo apt install lynis -y && sudo lynis audit system --report-file /tmp/lynis_internal.txt"
scp andromeda@$TARGET:/tmp/lynis_internal.txt ./

echo "=== ASSESSMENT COMPLETE ==="
echo "Review files: network_scan.txt, vulnerabilities.txt, web_scan.txt, lynis_internal.txt"
