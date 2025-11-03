# VM Deployment Guide

## Quick Deployment

### 1. Create Package
```bash
./create_package.sh
```

### 2. Transfer to VM
```bash
scp /tmp/snipe-po-tool-YYYYMMDD.tar.gz user@vm-ip:~/
```

### 3. Deploy on VM
```bash
tar -xzf snipe-po-tool-YYYYMMDD.tar.gz
cd snipe-po-tool-YYYYMMDD
./deploy.sh
```

### 4. Configure
```bash
sudo nano /opt/snipe-po-tool/.env
```

Add your Snipe-IT details:
```
SNIPE_URL=http://your-snipe-it-url
SNIPE_TOKEN=your-api-token
```

### 5. Access
- Web interface: `http://vm-ip:5001`
- Service status: `sudo systemctl status snipe-po-tool`

## Management

```bash
# Start/stop service
sudo systemctl start snipe-po-tool
sudo systemctl stop snipe-po-tool
sudo systemctl restart snipe-po-tool

# View logs
sudo journalctl -u snipe-po-tool -f

# Update application
cd /opt/snipe-po-tool
git pull
sudo systemctl restart snipe-po-tool
```

## Requirements

- Ubuntu/Debian VM
- Python 3.7+
- Internet access to Snipe-IT
- Port 5001 accessible
