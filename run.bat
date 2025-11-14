@echo off
REM Launch GloMAP Photogrammetry GUI
REM This batch file runs the Python application

echo ========================================
echo   GloMAP Photogrammetry GUI
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Run the application
python main.py

REM If application exits with error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   Application exited with an error
    echo ========================================
    pause
)
