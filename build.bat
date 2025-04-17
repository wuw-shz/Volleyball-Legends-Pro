@echo off
setlocal

echo Starting Volleyball Legends Pro build process...

:: Get the directory of this batch file (avoiding issues with special characters)
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: Run the build script with the correct path handling
python "%SCRIPT_DIR%\tools\build\build.py"

echo.
pause 