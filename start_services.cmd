@echo off

REM Up the provider in windows
start ollama serve

docker-compose up
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to start containers. Check Docker logs with 'docker compose logs'.
    echo Possible fixes: Ensure Docker Desktop is running or check if port 8080 is free.
    exit /b 1
)

timeout /t 10 /nobreak >nul