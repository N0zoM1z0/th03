@echo off
setlocal
where cmake >nul 2>nul
if errorlevel 1 goto missing
where ninja >nul 2>nul
if errorlevel 1 goto missing
where g++ >nul 2>nul
if errorlevel 1 goto missing
set "TH03_BUILD_DIR=%~dp0..\build\portable-win64"
cmake -S "%~dp0." -B "%TH03_BUILD_DIR%" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=g++
if errorlevel 1 exit /b 1
cmake --build "%TH03_BUILD_DIR%" --target th03-port64 --parallel 1
if errorlevel 1 exit /b 1
echo Built: %TH03_BUILD_DIR%\th03-port64.exe
exit /b 0
:missing
echo Install 64-bit MinGW-w64 GCC, CMake and Ninja, and add them to PATH.
exit /b 1
