@echo off

REM Up the provider in windows
start ollama serve

timeout /t 4 /nobreak >nul
for /f "tokens=*" %%i in ('docker ps -a -q') do docker stop %%i
echo All containers stopped

docker-compose up
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to start containers. Check Docker logs with 'docker compose logs'.
    echo Possible fixes: Ensure Docker Desktop is running or check if port 8080 is free.
    exit /b 1
)

timeout /t 10 /nobreak >nul