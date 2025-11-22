#!/bin/bash
echo "Installing Security Testing Requirements..."

# Update system
sudo apt update

# Install Python pip
sudo apt install python3-pip -y

# Install requirements
pip3 install -r requirements.txt

# Install system packages for some tools
sudo apt install nmap nikto hydra john -y

# Install Lynis from GitHub
git clone https://github.com/CISOfy/lynis
cd lynis
echo "Lynis installed in ./lynis/"

echo "Installation complete!"
echo "Available tools: nmap, nikto, lynis, and Python security libraries"
