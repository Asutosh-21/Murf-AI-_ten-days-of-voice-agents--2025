@echo off
echo NovaTrust Bank - Database Manager
echo =================================
echo.
echo 1. View database
echo 2. Show test customers
echo 3. Reset all cases
echo 4. Exit
echo.

:menu
set /p choice="Select option (1-4): "

if "%choice%"=="1" (
    echo.
    python show_database.py
    echo.
    goto menu
)

if "%choice%"=="2" (
    echo.
    python show_database.py test
    echo.
    goto menu
)

if "%choice%"=="3" (
    echo.
    set /p confirm="Reset all cases to pending? (y/n): "
    if /i "%confirm%"=="y" (
        python show_database.py reset
    )
    echo.
    goto menu
)

if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
)

echo Invalid option. Try again.
echo.
goto menu