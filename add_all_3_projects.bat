@echo off
REM Add All 3 Projects to GitHub Repo (Without Deleting Existing)

echo ========================================
echo Add All 3 Projects to GitHub
echo ========================================
echo.

cd "e:\ten-days-of-voice-agents-2025-main"

REM Initialize git if not already
if not exist ".git" (
    echo Initializing git...
    git init
)

REM Add all 3 project folders
echo Adding all 3 projects...
git add "Day 5 SDR Agent"
git add "Day 6 Fraud Alert Agent"
git add "Day 9 E-commerce Agent"
git add *.md
git add *.bat

REM Commit
echo Creating commit...
git commit -m "Add all 3 AI Voice Agent projects - SDR, Fraud Detection, E-commerce"

REM Add remote
echo Setting remote...
git remote remove origin 2>nul
git remote add origin https://github.com/Asutosh-21/Murf-AI-_ten-days-of-voice-agents--2025.git

REM Push (this will add to existing files, not replace)
echo Pushing to GitHub...
git branch -M main
git pull origin main --allow-unrelated-histories
git push -u origin main

echo.
echo ========================================
echo SUCCESS! All 3 projects added to GitHub
echo ========================================
echo.
echo Check: https://github.com/Asutosh-21/Murf-AI-_ten-days-of-voice-agents--2025
echo.
pause
