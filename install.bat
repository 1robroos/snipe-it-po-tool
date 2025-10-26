@echo off
echo 🛒 Installing Snipe-IT Purchase Order Tool...

REM Install Python dependencies
echo 📦 Installing dependencies...
pip install flask python-dotenv requests weasyprint jinja2

REM Create .env file if it doesn't exist
if not exist .env (
    echo ⚙️ Creating .env configuration file...
    copy .env.example .env
    echo ❗ Please edit .env file with your Snipe-IT URL and API token
)

echo ✅ Installation complete!
echo.
echo 📋 How to use:
echo.
echo 🖱️ EASIEST - Double-click: start_web_app.bat
echo.
echo 🌐 Manual Web Interface:
echo    python interactive_web_app.py
echo    Open browser to: http://localhost:5001
echo.
echo ⚡ Command Line:
echo    python interactive_cli.py
echo.
echo ⚙️ Don't forget to edit .env with your Snipe-IT details!
echo.
pause
