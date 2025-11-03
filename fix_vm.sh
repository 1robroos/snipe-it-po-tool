#!/bin/bash

# Quick fix for WeasyPrint dependencies on VM

echo "🔧 Installing missing WeasyPrint dependencies..."

sudo apt update
sudo apt install -y \
    libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    libfontconfig1 libcairo2 libgdk-pixbuf2.0-0 \
    libgtk-3-0 libxml2 libxslt1.1

echo "🔄 Restarting service..."
sudo systemctl restart snipe-po-tool

echo "✅ Fixed! Check status:"
sudo systemctl status snipe-po-tool
