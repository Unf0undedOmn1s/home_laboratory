# Home Lab Services Overview

This document outlines the core services, network configuration, and security measures implemented on the self-hosted Ubuntu Server, which acts as the central hub for the Home Lab environment.


## Security and Access Layer

### 1. Tailscale VPN (Virtual Private Network)

* **Purpose:** Establishes a secure, private network (Tailnet) that connects all authorized devices regardless of their physical location (LAN, WAN, 4G, etc.).
* **Access Method:** All remote access to the server's services is conducted exclusively through the **Tailscale IP address** (`100.x.x.x`).
* **Benefit:** This configuration eliminates the need for port forwarding on the main router, drastically simplifying remote access and enhancing security.

### 2. SFTP Service Restriction (SSH Daemon)

* **Service:** Secure File Transfer Protocol (SFTP), provided by the OpenSSH server (`sshd`).
* **Configuration:** The `sshd_config` file has been modified to restrict the server to listen only on the **Tailscale IP address**.
    * **Configuration File:** `/etc/ssh/sshd_config`
    * **Directive:** `ListenAddress <Server's Tailscale IP>`
* **Result:** SFTP access to files is possible **only** for devices connected to the Tailscale VPN. Attempts to connect using the LAN or public IP will be refused.

### 3. Fail2ban Intrusion Prevention

* **Purpose:** Protects services (primarily SSH/SFTP) from brute-force attacks by monitoring logs for repeated failed login attempts.
* **Configuration:**
    * **Jail:** `[sshd]` is enabled in `/etc/fail2ban/jail.local`.
    * **Ban Policy:** If a client exceeds **3 failed attempts** within a **10-minute** window, their IP is banned for **24 hours**.
    * **Exclusion:** All necessary Tailscale IP addresses (`100.x.x.x` range) are explicitly listed in the `ignoreip` directive to prevent accidental bans of legitimate users.


## Core Services

### 1. Pi-hole (Network-wide Ad Blocking)

* **Purpose:** DNS sinkhole that blocks advertisements and tracking requests at the network level, improving privacy and network speed.
* **Integration:** Configured as the primary DNS server for the local network or specific clients.
* **Access:** The admin panel is accessible via the server's IP address (e.g., `http://<LAN IP>/admin` or `http://<Tailscale IP>/admin`).

### 2. SFTP/File Hosting

* **Purpose:** Secure storage and transfer of files.
* **Access:** Restricted to Tailscale VPN members only, as detailed in the Security section.


## Monitoring and Management

### 1. Netdata (Real-Time Performance Monitoring)

* **Purpose:** Provides real-time metrics and visualization for the server's performance, including CPU usage, RAM, disk I/O, network traffic (including Tailscale interface), and service health.
* **Configuration:** The service is configured to bind its web interface exclusively to the **Tailscale IP address**.
    * **Access Address:** `http://<Server's Tailscale IP>:19999`
    * **Configuration File:** `/etc/netdata/netdata.conf` (under the `[web]` section).


## Planned Future Enhancements

The next major steps for the Home Lab infrastructure include:

1.  **Docker Integration:** Installation of Docker and Docker Compose to facilitate the easy deployment, isolation, and management of new services (e.g., Nextcloud, Jellyfin).
2.  **Automated Backup Solution:** Implementation of a robust CLI backup tool (such as Restic or BorgBackup) for automated, encrypted, and deduplicated backups of critical data and service configurations to an external drive or cloud storage.
