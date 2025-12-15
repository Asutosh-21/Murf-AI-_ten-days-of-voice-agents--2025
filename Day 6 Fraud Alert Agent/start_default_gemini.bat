@echo off
echo Starting NovaTrust Bank Fraud Agent (Default Gemini)
echo ==================================================
echo.

echo [1/3] Testing setup...
cd backend
python test_simple.py
if %errorlevel% neq 0 (
    echo Setup failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Starting backend with default Gemini model...
start "NovaTrust Backend" cmd /k "echo Starting with default Gemini... && uv run python src/agent.py dev"

echo.
echo [3/3] Starting frontend...
cd ..\frontend
start "NovaTrust Frontend" cmd /k "echo Starting frontend... && pnpm dev"

echo.
echo ==================================================
echo NovaTrust Bank Fraud Agent Started
echo ==================================================
echo.
echo Frontend: http://localhost:3000
echo.
echo Using default Gemini model (let LiveKit choose)
echo This should avoid model version conflicts.
echo.
echo Test customers:
echo - John Smith (answer: Johnson)
echo - Sarah Wilson (answer: Buddy)
echo - Michael Brown (answer: Chicago)
echo.
echo Press any key to close...
pause > nul