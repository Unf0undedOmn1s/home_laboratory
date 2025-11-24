#!/bin/bash
echo "Enhanced System Hardening"

# 0. Backup current state
echo "📊 Creating pre-hardening Lynis report..."
sudo lynis audit system --quick --report-file /tmp/lynis_before_hardening.txt

# 1. Enhanced firewall configuration
echo "🛡️ Configuring firewall..."
sudo ufw --force reset
sudo ufw --force enable
sudo ufw allow ssh comment 'SSH access'
sudo ufw allow from 100.64.0.0/10 comment 'Tailscale network'
sudo ufw default deny incoming
sudo ufw default deny forward
sudo ufw logging on

# 2. Automatic security updates with configuration
echo "🔧 Setting up automatic updates..."
sudo apt install unattended-upgrades apt-listchanges -y

# Configure automatic updates
sudo cat > /etc/apt/apt.conf.d/20auto-upgrades << EOF
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
EOF

sudo cat > /etc/apt/apt.conf.d/50unattended-upgrades << EOF
Unattended-Upgrade::Allowed-Origins {
    "\${distro_id}:\${distro_codename}";
    "\${distro_id}:\${distro_codename}-security";
    "\${distro_id}:\${distro_codename}-updates";
};
Unattended-Upgrade::AutoFixInterruptedDependencies "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF

# 3. Enhanced file permission cleanup
echo "📁 Securing file permissions..."
# Home directory permissions
find /home/$(whoami) -type f -perm /o+w -exec chmod o-w {} + 2>/dev/null
find /home/$(whoami) -type d -perm /o+w -exec chmod o-w {} + 2>/dev/null

# Secure SSH directory
chmod 700 /home/$(whoami)/.ssh
chmod 600 /home/$(whoami)/.ssh/* 2>/dev/null
chmod 644 /home/$(whoami)/.ssh/*.pub 2>/dev/null

# 4. Additional security configurations
echo "⚙️ Additional security tweaks..."

# Disable root login via SSH
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Enable UFW logging
sudo ufw logging medium

# Configure system limits
echo "* hard core 0" | sudo tee -a /etc/security/limits.conf
echo "fs.suid_dumpable = 0" | sudo tee -a /etc/sysctl.conf

# 5. Restart services
echo "🔄 Restarting services..."
sudo systemctl restart ssh
sudo systemctl enable unattended-upgrades
sudo systemctl start unattended-upgrades

# 6. Post-hardening verification
echo "📊 Running post-hardening Lynis scan..."
sudo lynis audit system --quick --report-file /tmp/lynis_after_hardening.txt

# 7. Compare results
echo " "
echo "HARDENING RESULTS"
echo "📈 Before hardening score:"
grep "Hardening Index" /tmp/lynis_before_hardening.txt | tail -1

echo "📈 After hardening score:"
grep "Hardening Index" /tmp/lynis_after_hardening.txt | tail -1

echo " "
echo "Enhanced hardening complete!"
echo "Firewall: Enhanced with logging"
echo "Updates: Fully automated"
echo "Permissions: Comprehensive cleanup"
echo "Reports: /tmp/lynis_before_hardening.txt"
echo "         /tmp/lynis_after_hardening.txt"

# Show specific improvements
echo " "
echo "🔍 Key improvements made:"
echo "• UFW with default deny policies"
echo "• Automatic security updates configured"
echo "• SSH directory secured"
echo "• File permissions tightened"
echo "• Root SSH login disabled"
