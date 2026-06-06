
@echo off
REM theZoo Web Sandbox - Windows Run Script
REM This script starts the FastAPI web sandbox server
REM Run this script from the theZoo root directory

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
REM Get the parent directory (theZoo root)
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Change to project root
cd /d "%PROJECT_ROOT%" || exit /b 1

echo ==============================================
echo   theZoo Web Sandbox
echo   A web-based interface for theZoo repository
echo ==============================================
echo.
echo Running from: %PROJECT_ROOT%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Error: FastAPI is not installed. Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Default configuration
set HOST=127.0.0.1
set PORT=8000

echo Starting theZoo Web Sandbox...
echo.
echo WARNING: This sandbox should ONLY be run in an isolated environment!
echo The theZoo repository contains LIVE MALWARE that can:
echo   - Infect your system
echo   - Spread to other machines
echo   - Cause permanent damage
echo.
echo Server Configuration:
echo   Host: %HOST%
echo   Port: %PORT%
echo.
echo Access the web interface at: http://%HOST%:%PORT%
echo.
echo Press Ctrl+C to stop the server
echo ==============================================
echo.

REM Start the server (use web_sandbox.main:app since we're in project root)
python -m uvicorn web_sandbox.main:app --host %HOST% --port %PORT% --reload

pause