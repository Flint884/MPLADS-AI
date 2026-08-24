@echo off
cd /d "%~dp0"
title MPLADS Sentinel AI
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
pause
