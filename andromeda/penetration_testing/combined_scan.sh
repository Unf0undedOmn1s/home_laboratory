# Step 1: Remote network scan
nmap -sS -sV -O $TARGET_IP > nmap_scan.txt

# Step 2: Web application scanning (if web services found)
nikto -h http://$TARGET_IP > nikto_scan.txt

# Step 3: SSH into target and run Lynis internally
ssh andromeda@$TARGET_IP "sudo lynis audit system --report-file /tmp/internal_audit.txt"

# Step 4: Retrieve the Lynis report
scp andromeda@$TARGET_IP/tmp/internal_audit.txt ./