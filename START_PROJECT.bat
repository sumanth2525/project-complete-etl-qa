@echo off
echo ============================================================
echo Bank Statement ETL Application - Starting...
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo Starting Flask Server...
echo ============================================================
echo.
echo Application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start the Flask application
python app.py

pause

