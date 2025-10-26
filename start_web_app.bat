@echo off
echo 🛒 Starting Snipe-IT Purchase Order Tool...
echo ================================================

REM Check if .env exists
if not exist .env (
    echo ❌ Configuration file .env not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

echo 🚀 Starting web interface...
echo 📱 The web page will open automatically
echo 🌐 Or manually go to: http://localhost:5001
echo.
echo 💡 To stop: Close this window
echo ================================================

REM Start web app
start /min python interactive_web_app.py

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:5001

echo Web interface is running...
echo Close this window to stop the application.
pause
