@echo off
echo ============================================
echo MongoDB Lab 165 - Windows 11 Setup
echo ============================================

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo Please download and install Python from python.org
    pause
    exit /b 1
)

REM Check if MongoDB is running
echo Checking MongoDB service...
tasklist /fi "imagename eq mongod.exe" | find "mongod.exe" >nul
if errorlevel 1 (
    echo WARNING: MongoDB is not running
    echo Starting MongoDB service...
    net start MongoDB
    if errorlevel 1 (
        echo ERROR: Could not start MongoDB service
        echo Please ensure MongoDB is properly installed
        pause
        exit /b 1
    )
)

REM Create virtual environment
echo Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

REM Create necessary directories
if not exist data mkdir data
if not exist exports mkdir exports
if not exist backup mkdir backup

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo Next steps:
echo 1. Import data: mongoimport --db my_data --collection open_data --type csv --headerline --file data\path_of_exile_ladder.csv
echo 2. Run application: python app.py
echo 3. Open browser: http://localhost:5000
echo.
pause
