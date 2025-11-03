#!/bin/bash

# Update VM with SSL verification fix

echo "🔧 Updating SSL verification support..."

# Copy updated files to VM
scp src/snipe_api.py interactive_web_app.py user@vm:/opt/snipe-po-tool/

# Add SSL setting to .env
echo "📝 Adding SSL verification setting..."
ssh user@vm "echo 'VERIFY_SSL=false' >> /opt/snipe-po-tool/.env"

# Restart service
echo "🔄 Restarting service..."
ssh user@vm "sudo systemctl restart snipe-po-tool"

echo "✅ Updated! SSL verification disabled."
