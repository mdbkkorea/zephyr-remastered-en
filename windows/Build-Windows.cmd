@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-Windows.ps1"
if errorlevel 1 echo BUILD FAILED. Read the error above.
pause
