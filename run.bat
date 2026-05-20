@echo off
echo Starting Intelligent Testing Automation Tool...
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Navigate to backend
cd backend

REM Run Flask app
echo Starting Flask server on http://localhost:5000
echo Open your browser and go to: http://localhost:5000
python app.py

pause
