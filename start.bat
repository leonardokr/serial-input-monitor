@echo off
REM Serial Input Monitor - Startup Script
REM Run this file to start the application
REM Author: Leonardo Klein

title Serial Input Monitor

echo ========================================
echo   Serial Input Monitor
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ and try again.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if main file exists
if not exist "src\main.py" (
    echo ERROR: src\main.py file not found!
    echo Check if you are in the correct project folder.
    pause
    exit /b 1
)

echo Python found - OK
echo.

REM Check and install dependencies if needed
if not exist "requirements.txt" (
    echo WARNING: requirements.txt not found
) else (
    echo Checking dependencies...
    python -m pip install -r requirements.txt --quiet --disable-pip-version-check
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo Dependencies checked - OK
)

echo.
echo Starting application...
echo.

REM Run application
python src\main.py

REM If we get here, the application was closed
echo.
echo Application closed.
pause
