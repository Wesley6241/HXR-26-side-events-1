@echo off
REM 直接安装依赖的批处理脚本（无需激活虚拟环境）
echo Installing dependencies...
venv\Scripts\python.exe -m pip install -r requirements.txt
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Dependencies installed successfully!
) else (
    echo.
    echo Failed to install dependencies.
    pause
)
