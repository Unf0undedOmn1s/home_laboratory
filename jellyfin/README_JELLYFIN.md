# Self-Hosted Jellyfin Media Server

This project documents the setup of a local Jellyfin media server using Docker on Ubuntu running inside a VirtualBox VM. The server allows streaming of movies and series within the local network.

## Requirements

- Ubuntu (running on VirtualBox)
- Docker and Docker Compose
- Media files (movies, series, music)
- Internet connection

## Installation Steps

### Step 1: Update the system
```bash
sudo apt update && sudo apt upgrade -y
```

## Install Docker
```bash
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
```

## Pull the latest Jellyfin Docker Image
`sudo docker pull jellyfin/jellyfin:latest`

## Run Jellyfin Container
```bash
sudo docker run -d \
  --name jellyfin \
  -p 8096:8096 \
  -v ~/jellyfin/config:/config \
  -v ~/jellyfin/media:/media \
  --restart=unless-stopped \
  jellyfin/jellyfin:latest
  ```

## Accessing Jellyfin
`http://<host-ip>:8096`

## Configuration
On first launch, create an admin account in Jellyfin.
1. Add your media libraries:
- Movies → `~/jellyfin/media/movies`
- Series → `~/jellyfin/media/series`
2. Start scanning your library.

## File Structure
```bash
~/jellyfin/
   ├── config/   # Jellyfin configuration files
   └── media/    # Media files
        ├── movies/
        └── series/
```

## Notes
- The container is set to restart automatically with --restart=unless-stopped.
- By default, the server is only accessible in the local network.
- For remote access, consider setting up a reverse proxy with HTTPS (NGINX or Caddy).

## Future Improvements
- Add HTTPS with a reverse proxy
- Use a custom domain name
- Automate with Docker Compose
- Add backup strategy for configuration and media