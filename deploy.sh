#!/bin/bash

# Snipe-IT Purchase Order Tool - VM Deployment Script
# Usage: ./deploy.sh

set -e

echo "🚀 Deploying Snipe-IT Purchase Order Tool..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root"
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git curl \
    libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    libfontconfig1 libcairo2 libgdk-pixbuf2.0-0 \
    libgtk-3-0 libxml2 libxslt1.1

# Create application directory
APP_DIR="/opt/snipe-po-tool"
echo "📁 Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "📋 Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env configuration file..."
    cp .env.example .env
    echo "📝 Please edit /opt/snipe-po-tool/.env with your Snipe-IT details"
fi

# Create systemd service
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/snipe-po-tool.service > /dev/null <<EOF
[Unit]
Description=Snipe-IT Purchase Order Tool
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python interactive_web_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable snipe-po-tool
sudo systemctl start snipe-po-tool

# Create nginx config (optional)
if command -v nginx &> /dev/null; then
    echo "🌐 Setting up nginx reverse proxy..."
    sudo tee /etc/nginx/sites-available/snipe-po-tool > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF
    sudo ln -sf /etc/nginx/sites-available/snipe-po-tool /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
fi

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit configuration: sudo nano $APP_DIR/.env"
echo "2. Check service status: sudo systemctl status snipe-po-tool"
echo "3. View logs: sudo journalctl -u snipe-po-tool -f"
echo "4. Access web interface: http://$(hostname -I | awk '{print $1}'):5001"
echo ""
echo "🔧 Management commands:"
echo "  Start:   sudo systemctl start snipe-po-tool"
echo "  Stop:    sudo systemctl stop snipe-po-tool"
echo "  Restart: sudo systemctl restart snipe-po-tool"
