#!/bin/bash
# Easy startup script for Snipe-IT Purchase Order Tool

echo "🛒 Starting Snipe-IT Purchase Order Tool..."
echo "================================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Configuration file .env not found!"
    echo "Please run ./install.sh first"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if configured
if grep -q "your-api-token-here" .env; then
    echo "⚠️  API token not configured!"
    echo "Please edit .env file with your Snipe-IT details"
    read -p "Press Enter to continue anyway..."
fi

echo "🚀 Starting web interface..."
echo "📱 The web page will open automatically"
echo "🌐 Or manually go to: http://localhost:5001"
echo ""
echo "💡 To stop: Press Ctrl+C in this window"
echo "================================================"

# Start web app and open browser
python3 interactive_web_app.py &
WEB_PID=$!

# Wait a moment for server to start
sleep 3

# Try to open browser (works on most Linux desktops)
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:5001
elif command -v gnome-open > /dev/null; then
    gnome-open http://localhost:5001
elif command -v firefox > /dev/null; then
    firefox http://localhost:5001 &
else
    echo "Please open your browser and go to: http://localhost:5001"
fi

# Wait for web app to finish
wait $WEB_PID
