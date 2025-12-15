@echo off
echo NovaTrust Bank - Telephony Fraud Agent
echo =======================================
echo.

echo [1/4] Validating telephony configuration...
cd backend
python telephony_config.py
if %errorlevel% neq 0 (
    echo Configuration validation failed!
    pause
    exit /b 1
)

echo.
echo [2/4] Testing database...
python test_simple.py
if %errorlevel% neq 0 (
    echo Database test failed!
    pause
    exit /b 1
)

echo.
echo [3/4] Starting telephony agent...
start "NovaTrust Telephony Agent" cmd /k "echo Starting telephony fraud agent... && uv run python src/telephony_agent.py dev"

echo.
echo [4/4] Starting web interface (optional)...
cd ..\frontend
start "NovaTrust Web Interface" cmd /k "echo Starting web interface... && pnpm dev"

echo.
echo =======================================
echo NovaTrust Telephony Agent Started
echo =======================================
echo.
echo TELEPHONY FEATURES:
echo - Real phone call integration
echo - Enhanced fraud detection workflow
echo - Automatic database updates
echo - Call logging and metrics
echo.
echo WEB INTERFACE: http://localhost:3000
echo.
echo PHONE INTEGRATION:
echo - Configure your SIP trunk to route calls to LiveKit
echo - Use LiveKit Cloud phone numbers
echo - Test with web interface first
echo.
echo Test customers (same as web):
echo - John Smith (answer: Johnson)
echo - Sarah Wilson (answer: Buddy)
echo - Michael Brown (answer: Chicago)
echo.
echo Press any key to close...
pause > nul