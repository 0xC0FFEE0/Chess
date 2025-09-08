#  Chess Web App - Home Server Deployment Guide

This guide provides step-by-step instructions for deploying the Chess Web App on your home server for 24/7 access across your network.

##  Pre-Deployment Checklist

- [ ] Python 3.7+ installed on your server
- [ ] Stockfish chess engine installed
- [ ] Network access configured
- [ ] Firewall ports opened
- [ ] Static IP or DDNS configured (optional)

##  Server Requirements

### Minimum Hardware
- **CPU**: 1 GHz single-core processor
- **RAM**: 1GB available memory
- **Storage**: 500MB free space
- **Network**: Ethernet or Wi-Fi connection

### Recommended Hardware
- **CPU**: 2 GHz dual-core processor  
- **RAM**: 2GB available memory
- **Storage**: 2GB free space
- **Network**: Gigabit Ethernet connection

##  Installation Steps

### Step 1: Download and Setup
```bash
# Navigate to your preferred directory
cd /opt  # Linux/macOS
# or 
cd C:\Applications  # Windows

# Clone or extract the chess-webapp folder
# Ensure you have the complete chess-webapp directory
```

### Step 2: Install Python Dependencies
```bash
# Navigate to chess-webapp directory
cd chess-webapp

# Install required packages
pip install -r requirements.txt

# For system-wide installation (Linux)
sudo pip3 install -r requirements.txt
```

### Step 3: Install Stockfish Engine

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install stockfish
```

#### On CentOS/RHEL:
```bash
sudo yum install stockfish
# or
sudo dnf install stockfish
```

#### On Windows:
1. Download from https://stockfishchess.org/download/
2. Extract to `C:\Program Files\Stockfish\`
3. Add to system PATH or place `stockfish.exe` in project directory

#### On macOS:
```bash
# Using Homebrew
brew install stockfish

# Using MacPorts
sudo port install stockfish
```

### Step 4: Test Installation
```bash
# Test Python dependencies
python -c "import flask, chess, stockfish; print('Dependencies OK')"

# Test Stockfish
stockfish
# Should open Stockfish UCI interface (type 'quit' to exit)
```

##  Network Configuration

### Find Your Server IP Address
```bash
# Linux/macOS
ip addr show  # or ifconfig
hostname -I

# Windows
ipconfig
```

### Configure Firewall

#### Linux (UFW):
```bash
# Allow chess app port
sudo ufw allow 5000

# Check status
sudo ufw status
```

#### Linux (firewalld):
```bash
# Allow port permanently
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

#### Windows:
1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Create new "Inbound Rule"
4. Allow TCP port 5000
5. Name it "Chess Web App"

## 🔧 Production Deployment

### Option 1: Simple Manual Start
```bash
cd chess-webapp
python app.py
```
**Pros**: Simple, immediate
**Cons**: Stops when terminal closes, no auto-restart

### Option 2: Background Process (Linux/macOS)
```bash
# Start in background
cd chess-webapp
nohup python app.py > chess.log 2>&1 &

# Check if running
ps aux | grep app.py

# Stop the process
pkill -f app.py
```

### Option 3: Systemd Service (Linux - Recommended)

#### Create Service File:
```bash
sudo nano /etc/systemd/system/chess-webapp.service
```

#### Service Configuration:
```ini
[Unit]
Description=Chess Web App
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
Group=YOUR_GROUP
WorkingDirectory=/full/path/to/chess-webapp
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable chess-webapp

# Start the service
sudo systemctl start chess-webapp

# Check status
sudo systemctl status chess-webapp

# View logs
journalctl -u chess-webapp -f
```

### Option 4: Windows Service
Use tools like NSSM (Non-Sucking Service Manager):
```cmd
# Download and install NSSM
nssm install "Chess Web App"
# Configure path to python.exe and app.py
# Start the service
```

##  Security Configuration

### Change Default Settings
Edit [`app.py`](app.py:8):
```python
# Change the secret key
app.config['SECRET_KEY'] = 'your-secure-random-key-here'

# For production, disable debug mode
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

### Optional: Reverse Proxy Setup (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

##  External Access Setup (Optional)

### Router Configuration
1. **Port Forwarding**:
   - Forward external port 8080 → internal port 5000
   - Point to your server's local IP

2. **Dynamic DNS** (if no static IP):
   - Use services like No-IP, DynDNS, or Duck DNS
   - Configure your router to update DDNS

### SSL/HTTPS Setup
For external access, consider SSL:
```bash
# Using Let's Encrypt with Certbot
sudo apt install certbot
sudo certbot --standalone -d your-domain.com
```

##  Monitoring and Maintenance

### Check Application Status
```bash
# Check if service is running
sudo systemctl status chess-webapp

# View application logs
tail -f /path/to/chess-webapp/chess.log

# Check port usage
netstat -tlnp | grep 5000
```

### Log Rotation
Create [`/etc/logrotate.d/chess-webapp`](path):
```
/path/to/chess-webapp/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 username username
}
```

### Backup Strategy
```bash
# Backup application
tar -czf chess-webapp-backup-$(date +%Y%m%d).tar.gz chess-webapp/

# Automated backup script
echo "0 2 * * * tar -czf /backups/chess-$(date +\%Y\%m\%d).tar.gz /opt/chess-webapp/" | crontab -
```

##  Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python and dependencies
python --version
pip list | grep -E "(flask|chess|stockfish)"

# Check port availability
netstat -tlnp | grep 5000
```

#### Can't Access from Other Devices
```bash
# Verify server is listening on all interfaces
netstat -tlnp | grep ":5000"
# Should show 0.0.0.0:5000, not 127.0.0.1:5000

# Test local access
curl http://localhost:5000

# Test network access from another device
curl http://YOUR_SERVER_IP:5000
```

#### Stockfish Not Working
```bash
# Verify Stockfish installation
which stockfish
stockfish

# Check if accessible to Python
python -c "from stockfish import Stockfish; print('OK')"
```

#### Performance Issues
```bash
# Check system resources
htop  # or top
df -h  # disk space
free -h  # memory usage

# Monitor application
ps aux | grep python
```

### Log Analysis
```bash
# Application logs
tail -f chess.log

# System logs (if using systemd)
journalctl -u chess-webapp -f

# Network connections
netstat -an | grep 5000
```

##  Access URLs

Once deployed, access your chess app at:
- **Local**: http://localhost:5000
- **Network**: http://YOUR_SERVER_IP:5000
- **External**: http://YOUR_EXTERNAL_IP:8080 (if port forwarded)
- **Domain**: http://your-domain.com (if configured)

##  Updates and Maintenance

### Updating the Application
```bash
# Stop the service
sudo systemctl stop chess-webapp

# Backup current version
cp -r chess-webapp chess-webapp-backup

# Update files (copy new version)
# ...

# Restart service
sudo systemctl start chess-webapp
```

### Health Monitoring
Create a simple health check script:
```bash
#!/bin/bash
# health-check.sh
if curl -f http://localhost:5000 > /dev/null 2>&1; then
    echo "Chess app is running"
else
    echo "Chess app is down - restarting"
    sudo systemctl restart chess-webapp
fi
```

Run via cron:
```bash
# Check every 5 minutes
*/5 * * * * /path/to/health-check.sh
```

---

##  Quick Deployment Summary

1. **Install**: Python + dependencies + Stockfish
2. **Configure**: Firewall + network settings  
3. **Deploy**: Choose deployment method (manual/service)
4. **Test**: Access from multiple devices
5. **Secure**: Change secrets, consider SSL
6. **Monitor**: Set up logging and health checks

Your chess web app is now ready for 24/7 home server deployment! 🏠♛