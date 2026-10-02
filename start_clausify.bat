@echo off
title Clausify AI Platform Launcher
echo ========================================================
echo           STARTING CLAUSIFY AI PLATFORM
echo ========================================================

cd /d "%~dp0"

echo [1/3] Starting FastAPI Backend on Port 8000...
start "Clausify Backend (Port 8000)" cmd /k "cd backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo [2/3] Starting Vite React Frontend on Port 5173...
start "Clausify Frontend (Port 5173)" cmd /k "cd frontend && node node_modules\vite\bin\vite.js"

echo Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak > nul

echo [3/3] Starting Unified Gateway on Port 8080...
start "Clausify Gateway (Port 8080)" cmd /k "cd backend && venv\Scripts\python.exe gateway_8080.py"

timeout /t 2 /nobreak > nul

echo Launching Clausify in default browser...
start http://localhost:8080

echo ========================================================
echo Clausify is running!
echo Access Portal: http://localhost:8080
echo API Docs:      http://localhost:8000/docs
echo ========================================================
