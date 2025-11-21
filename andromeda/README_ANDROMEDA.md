# Andromeda Server Documentation
## System Overview
Andromeda functions as a secure edge node providing DNS filtering, network monitoring, and system analytics. It integrates Pi-hole, Prometheus, Grafana, and Tailscale into a unified stack for privacy-oriented network management.

## Core Components
| Component | Purpose | Port |
|------------|----------|------|
| Pi-hole | DNS-based ad and tracker blocking | 80 |
| Prometheus | Metrics collection and scraping | 9090 |
| Grafana | Data visualization and dashboarding | 3000 |
| Flask Dashboard | Custom web interface for file and system management | 5000 |
| Tailscale | Secure private network connectivity | - |

## Network Access
Access to Andromeda services is available through both the local network and the Tailscale mesh VPN.

- Local access:
  - Pi-hole: `http://<ip_address>/admin`
  - Prometheus: `http://ip_address:9090`
  - Grafana: `http://ip_address:3000`
  - Flask Dashboard: `http://ip_address:5000`

- Remote access via Tailscale:
  - Example: `http://andromeda.tailnet-name.ts.net:3000`

## Prometheus Configuration
File: `/etc/prometheus/prometheus.yml`

```yaml
scrape_configs:
  - job_name: 'andromeda'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'pihole'
    static_configs:
      - targets: ['localhost:9617']
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

## Grafana Setup
- Default credentials: `admin / admin`
- Prometheus data source: `http://localhost:9090`
- Dashboards:
  - Pi-hole statistics
  - System resource metrics
  - Power and energy monitoring

## Flask Dashboard
A Python Flask-based web application provides a management layer for Andromeda.

Features:
- File upload and download
- Real-time power monitoring using `powerstat`
- System statistics API endpoints
- User authentication

Runs via:
```bash
python3 app.py
```

## Security
- Tailscale restricts remote access to authenticated devices.
- Pi-hole provides network-level filtering.
- Flask interface protected by user sessions.
- Grafana limited to local or Tailscale access.

## Maintenance
System updates:
```bash
sudo apt update && sudo apt upgrade -y
```

Service restarts:
```bash
sudo systemctl restart pihole-FTL
sudo systemctl restart prometheus
sudo systemctl restart grafana-server
```

## Future Work
- Integrate Telegram alerts for key events.
- Export metrics to Orion for centralized analytics.
- Add backup sync through Tailscale or rsync.
