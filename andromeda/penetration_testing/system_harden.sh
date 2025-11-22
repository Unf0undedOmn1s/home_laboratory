#!/bin/bash
echo "Quick System Hygiene"

# 1. Basic firewall
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow from 100.64.0.0/10

# 2. Automatic security updates
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades

# 3. Quick file permission cleanup
find /home/$(whoami) -type f -perm /o+w -exec chmod o-w {} + 2>/dev/null

echo " Basic hygiene complete!"
echo "Firewall: Enabled, Updates: Automated, Permissions: Cleaned"
