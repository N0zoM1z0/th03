@echo off
setlocal
cd /d "%~dp0"
for %%F in (th03-port64.exe th03.hdi FREECG98.BMP ym2608_adpcm_rom.bin) do if not exist "%~dp0%%F" goto missing
start "" "%~dp0th03-port64.exe" --hdi "%~dp0th03.hdi" --font-bmp "%~dp0FREECG98.BMP" --save-dir "%~dp0save-normal" --audio --pmd-driver pmd86 --opna-rom "%~dp0ym2608_adpcm_rom.bin"
exit /b 0
:missing
echo Add th03.hdi, FREECG98.BMP and ym2608_adpcm_rom.bin beside th03-port64.exe.
echo Use Play-silent.bat to play without sound or a rhythm ROM.
pause
exit /b 1
