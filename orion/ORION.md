# Orion Documentation
## System Overview
Orion operates as a centralized analytics and monitoring node. It runs Prometheus and Grafana, with a custom visualization layer and malware scanning engine, and communicates securely with Andromeda through Tailscale.

## Core Components
| Component | Purpose | Port |
|------------|----------|------|
| Prometheus | Data collection and aggregation | 9090 |
| Grafana | Visualization and dashboarding | 3000 |
| Web Visualization | Custom HTML/JS/CSS dashboard for real-time analytics | 8080 |
| Malware Scanner | Automated file and process scanning | - |
| Tailscale | Secure connectivity with Andromeda and other nodes | - |

## Network Configuration
Orion connects to Andromeda and other nodes through the Tailscale mesh network.

Example Prometheus job:
```yaml
- job_name: 'andromeda_metrics'
  static_configs:
    - targets: ['100.x.x.x:9090']
```

## Prometheus and Grafana
Prometheus scrapes both local metrics and those from Andromeda.

Example configuration:
```yaml
scrape_configs:
  - job_name: 'orion_system'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'andromeda_metrics'
    static_configs:
      - targets: ['100.x.x.x:9090']
```

Grafana connects to Prometheus at `http://localhost:9090` and includes dashboards for:
- Node performance metrics
- Network traffic and latency
- Power and system usage (imported from Andromeda)
- Malware detection summary

## Custom Visualization Layer
The custom frontend, located at `/srv/orion-dashboard/`, uses HTML, CSS, and JavaScript to display Prometheus metrics through the HTTP API.

Example:
```javascript
fetch('http://localhost:9090/api/v1/query?query=node_cpu_seconds_total')
  .then(res => res.json())
  .then(data => renderChart(data));
```

## Malware Scanning Engine
The malware scanner (`/opt/orion/scanner.py`) performs periodic scans using `clamav` and `yara` signatures.

Metrics exported to Prometheus:
```
malware_scans_total 120
malware_detections_total 2
last_scan_timestamp 1720001234
```

Cron example:
```bash
*/10 * * * * /usr/bin/python3 /opt/orion/scanner.py
```

## Security
- Access via Tailscale network only.
- Grafana roles for admin and viewer users.
- Scanner runs in isolated environment.
- Regular update of malware signatures.

## Maintenance
Update services:
```bash
sudo systemctl restart prometheus
sudo systemctl restart grafana-server
```

Update scanner definitions:
```bash
sudo freshclam
```

## Future Work
- Telegram integration for scan alerts.
- Advanced anomaly detection dashboard.
- Automated data sync with Andromeda.
