@echo off
REM Batch file to start the Large File Scanner application

REM Navigate to the project directory
cd /d %~dp0

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    pause
    exit /b 1
)

REM Start the Python server in the background
echo Starting Python server...
start "" python server.py

REM Wait for the server to initialize (adjust delay if necessary)
echo Waiting for the server to start...
timeout /t 5 >nul

REM Open the HTML frontend in the default web browser
echo Opening the application in your browser...
start http://localhost:8000/

echo Application is now running. Close this window to stop the server.
pause
