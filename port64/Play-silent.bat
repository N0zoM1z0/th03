@echo off
setlocal
cd /d "%~dp0"
for %%F in (th03-port64.exe th03.hdi FREECG98.BMP) do if not exist "%~dp0%%F" goto missing
start "" "%~dp0th03-port64.exe" --hdi "%~dp0th03.hdi" --font-bmp "%~dp0FREECG98.BMP" --save-dir "%~dp0save-normal" --mute
exit /b 0
:missing
echo Add th03.hdi and FREECG98.BMP beside th03-port64.exe.
pause
exit /b 1
