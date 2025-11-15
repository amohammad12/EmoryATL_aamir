@echo off
echo ========================================
echo   Pirate Karaoke Backend Launcher
echo   Windows Startup Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if MongoDB is running
echo Checking MongoDB...
sc query MongoDB | find "RUNNING" > nul
if %errorlevel% neq 0 (
    echo WARNING: MongoDB is not running!
    echo Starting MongoDB...
    net start MongoDB
    timeout /t 2 > nul
)
echo [OK] MongoDB is running

REM Check if Redis is running (try to ping)
echo Checking Redis...
redis-cli ping > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Redis is not running!
    echo Starting Redis in new window...
    start "Redis Server" cmd /k redis-server
    timeout /t 3 > nul
) else (
    echo [OK] Redis is running
)

echo.
echo ========================================
echo   Starting Application Services
echo ========================================
echo.

REM Start Celery Worker
echo Starting Celery Worker...
start "Celery Worker" cmd /k "cd /d %~dp0 && venv\Scripts\activate && celery -A app.tasks worker --loglevel=info --pool=solo"
timeout /t 3 > nul

REM Start FastAPI Server
echo Starting FastAPI Server...
start "FastAPI Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 > nul

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Services Running:
echo   MongoDB:  http://localhost:27017
echo   Redis:    localhost:6379
echo   API:      http://localhost:8000
echo.
echo Open your browser: http://localhost:8000
echo.
echo To test API:
echo   POST http://localhost:8000/api/generate
echo   Body: {"word": "ship"}
echo.
echo Press any key to open API in browser...
pause > nul

REM Open browser
start http://localhost:8000

echo.
echo Startup complete!
echo Keep all windows open for the app to work.
echo Press CTRL+C in any window to stop that service.
echo.
pause
