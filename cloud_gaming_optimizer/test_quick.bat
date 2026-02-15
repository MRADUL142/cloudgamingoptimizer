@echo off
REM Quick Test Suite for Cloud Gaming Optimizer - Windows Batch Script

echo.
echo ================================================================================
echo Cloud Gaming Performance Optimizer - Quick Test
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

echo ================================================================================
echo Running Quick Test Suite...
echo ================================================================================
echo.

python test_quick.py

if errorlevel 1 (
    echo.
    echo Test suite failed. Check errors above.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo Testing Complete!
    echo ================================================================================
    echo.
    echo To continue testing:
    echo   - Run examples: python examples.py
    echo   - Run dashboard: python main.py --mode dashboard --interval 2
    echo   - Collect data: python main.py --mode collect --duration 30
    echo   - Read TESTING.md for more test options
    echo.
    pause
)
