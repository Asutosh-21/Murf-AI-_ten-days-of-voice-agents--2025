@echo off
REM Delete All Files from GitHub Repo

echo ========================================
echo WARNING: Delete All Files from GitHub
echo ========================================
echo.
echo This will DELETE ALL FILES from:
echo https://github.com/Asutosh-21/Murf-AI-_ten-days-of-voice-agents--2025
echo.
echo Are you ABSOLUTELY SURE?
set /p confirm="Type YES to confirm: "

if /i not "%confirm%"=="YES" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Deleting all files from GitHub...
echo.

cd "e:\ten-days-of-voice-agents-2025-main"

REM Initialize empty repo
git init

REM Create empty commit
git commit --allow-empty -m "Clear repository"

REM Force push to delete everything
git remote remove origin 2>nul
git remote add origin https://github.com/Asutosh-21/Murf-AI-_ten-days-of-voice-agents--2025.git
git branch -M main
git push -u origin main --force

echo.
echo ========================================
echo All files deleted from GitHub!
echo ========================================
echo.
echo Your repo is now empty.
echo Check: https://github.com/Asutosh-21/Murf-AI-_ten-days-of-voice-agents--2025
echo.
pause
