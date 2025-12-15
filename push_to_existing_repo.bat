@echo off
REM Push All 3 Projects to Existing GitHub Repo

echo ========================================
echo Push to Existing GitHub Repo
echo ========================================
echo.

set /p REPO_URL="Enter your existing GitHub repo URL: "

if "%REPO_URL%"=="" (
    echo ERROR: No repo URL provided!
    pause
    exit /b 1
)

echo.
echo Pushing to: %REPO_URL%
echo.

REM Initialize git if not already
if not exist ".git" (
    echo Initializing git...
    git init
)

REM Add all files
echo Adding all files...
git add .

REM Commit
echo Creating commit...
git commit -m "Add 3 AI Voice Agent Projects - SDR, E-commerce, Fraud Detection"

REM Add remote (remove if exists)
echo Setting remote...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

REM Push
echo Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ========================================
echo SUCCESS! Projects pushed to GitHub
echo ========================================
echo.
echo Check your repo: %REPO_URL%
echo.
pause
