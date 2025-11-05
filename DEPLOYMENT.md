# 📋 Snipe-IT Purchase Order Tool - Deployment Guide

## 🎯 Overview

This guide covers deployment of the Snipe-IT Purchase Order Tool on virtual machines for both test and production environments.

## 🏗️ Architecture

- **Web Interface**: Flask application on port 5001
- **PDF Generation**: Reportlab for stable PDF creation
- **Data Storage**: JSON file for PO counter persistence
- **Service Management**: Systemd service for automatic startup

## 🚀 Quick Deployment

### 1. Create Deployment Package
```bash
cd /path/to/snipe-po-tool
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

## 🧪 Test Environment Setup

### Characteristics
- Self-signed SSL certificates
- Development/testing purposes
- SSL verification disabled

### Configuration
```bash
sudo nano /opt/snipe-po-tool/.env
```

```env
SNIPE_URL=https://test-snipe-it.company.com
SNIPE_TOKEN=your-test-api-token-here
VERIFY_SSL=false
```

### Access
- Web Interface: `http://test-vm-ip:5001`
- Service Status: `sudo systemctl status snipe-po-tool`

## 🏭 Production Environment Setup

### Characteristics
- Valid SSL certificates
- Live business operations
- SSL verification enabled

### Configuration
```bash
sudo nano /opt/snipe-po-tool/.env
```

```env
SNIPE_URL=https://snipe-it.company.com
SNIPE_TOKEN=your-production-api-token-here
VERIFY_SSL=true
```

### Access
- Web Interface: `http://prod-vm-ip:5001`
- Optional: Setup nginx reverse proxy for port 80

## 🔧 Service Management

### Basic Commands
```bash
# Start service
sudo systemctl start snipe-po-tool

# Stop service
sudo systemctl stop snipe-po-tool

# Restart service
sudo systemctl restart snipe-po-tool

# Check status
sudo systemctl status snipe-po-tool

# View logs
sudo journalctl -u snipe-po-tool -f
```

### Service Configuration
Location: `/etc/systemd/system/snipe-po-tool.service`

```ini
[Unit]
Description=Snipe-IT Purchase Order Tool
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/snipe-po-tool
Environment=PATH=/opt/snipe-po-tool/venv/bin
ExecStart=/opt/snipe-po-tool/venv/bin/python interactive_web_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📁 File Structure

```
/opt/snipe-po-tool/
├── interactive_web_app.py     # Main web application
├── interactive_cli.py         # Command line interface
├── po_counter.py              # PO numbering system
├── .env                       # Configuration file
├── requirements.txt           # Python dependencies
├── venv/                      # Python virtual environment
├── src/                       # Source modules
│   ├── snipe_api.py          # Snipe-IT API client
│   └── pdf_generator.py      # PDF generation
├── templates/                 # HTML templates
├── static/                    # Static files (company header)
└── data/                      # Data storage
    └── po_counter.json       # PO counter persistence
```

## 🔐 Security Considerations

### Test Environment
- SSL verification disabled for self-signed certificates
- Suitable for internal testing only
- Should not be exposed to public internet

### Production Environment
- SSL verification enabled for security
- Valid certificates required
- Consider firewall rules and access controls

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Create new package
./create_package.sh

# Deploy to VM
scp /tmp/snipe-po-tool-YYYYMMDD.tar.gz user@vm-ip:~/
tar -xzf snipe-po-tool-YYYYMMDD.tar.gz
cd snipe-po-tool-YYYYMMDD

# Stop service
sudo systemctl stop snipe-po-tool

# Backup current installation
sudo cp -r /opt/snipe-po-tool /opt/snipe-po-tool.backup

# Copy new files (preserve .env and data/)
sudo cp -r . /opt/snipe-po-tool/
sudo cp /opt/snipe-po-tool.backup/.env /opt/snipe-po-tool/
sudo cp -r /opt/snipe-po-tool.backup/data/ /opt/snipe-po-tool/

# Restart service
sudo systemctl start snipe-po-tool
```

### Backup Important Data
```bash
# Backup PO counter
sudo cp /opt/snipe-po-tool/data/po_counter.json ~/po_counter_backup.json

# Backup configuration
sudo cp /opt/snipe-po-tool/.env ~/env_backup
```

## 🐛 Troubleshooting

### Common Issues

**Service won't start:**
```bash
sudo journalctl -u snipe-po-tool --no-pager -n 20
```

**SSL Certificate errors:**
- Test: Set `VERIFY_SSL=false`
- Production: Ensure valid certificates

**Permission errors:**
```bash
sudo chown -R your-user:your-user /opt/snipe-po-tool
```

**Port already in use:**
```bash
sudo lsof -i :5001
sudo kill <PID>
```

### Log Locations
- Service logs: `sudo journalctl -u snipe-po-tool`
- Application logs: Check console output in service logs

## 📊 Monitoring

### Health Checks
- Web interface accessibility: `curl http://vm-ip:5001`
- Service status: `systemctl is-active snipe-po-tool`
- Disk space: `df -h /opt/snipe-po-tool`

### Performance
- Memory usage: `ps aux | grep python`
- Process status: `systemctl status snipe-po-tool`

## 🔧 System Requirements

### Minimum Requirements
- Ubuntu/Debian Linux
- Python 3.7+
- 512MB RAM
- 1GB disk space
- Network access to Snipe-IT instance

### Recommended
- 1GB+ RAM
- 2GB+ disk space
- Regular backups of PO counter data
