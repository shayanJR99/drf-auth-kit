@echo off

title DRF Auth Kit Launcher

docker info > nul 2>&1

if %errorlevel% neq 0 (
    echo Docker Desktop is not running!
    pause
    exit
)

echo Starting containers...

docker compose up -d --build


echo Waiting for database...

timeout /t 5


echo Applying migrations...

docker compose exec backend python manage.py migrate


echo Done!

echo.
echo Frontend:
echo http://localhost:5173

echo Backend:
echo http://localhost:8000

echo SMTP:
echo http://localhost:5000


pause