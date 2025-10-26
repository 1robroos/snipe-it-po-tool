#!/bin/bash
# Installation script for Snipe-IT Purchase Order Tool

echo "🛒 Installing Snipe-IT Purchase Order Tool..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip3 install flask python-dotenv requests weasyprint jinja2

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env configuration file..."
    cp .env.example .env
    echo "❗ Please edit .env file with your Snipe-IT URL and API token"
fi

# Make scripts executable
chmod +x *.py *.sh

# Install desktop launcher (optional)
if [ -d "$HOME/Desktop" ]; then
    echo "🖥️ Installing desktop launcher..."
    cp Snipe-IT-PO-Tool.desktop "$HOME/Desktop/"
    chmod +x "$HOME/Desktop/Snipe-IT-PO-Tool.desktop"
    echo "✅ Desktop shortcut created"
fi

echo "✅ Installation complete!"
echo ""
echo "📋 How to use:"
echo ""
echo "🖱️ EASIEST - Double-click desktop icon (if available)"
echo "   Or run: ./start_web_app.sh"
echo ""
echo "🌐 Manual Web Interface:"
echo "   python3 interactive_web_app.py"
echo "   Open browser to: http://localhost:5001"
echo ""
echo "⚡ Command Line:"
echo "   python3 interactive_cli.py"
echo ""
echo "🔄 Automatic (All assets per supplier):"
echo "   python3 create_supplier_specific_po.py"
echo ""
echo "🧪 Test connection:"
echo "   python3 test_integration.py"
echo ""
echo "⚙️ Don't forget to edit .env with your Snipe-IT details!"
