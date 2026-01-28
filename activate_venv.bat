@echo off
REM 激活虚拟环境的批处理脚本
setlocal

REM 设置虚拟环境路径
set "VIRTUAL_ENV=%~dp0venv"

REM 检查虚拟环境是否存在
if not exist "%VIRTUAL_ENV%\Scripts\python.exe" (
    echo Error: Virtual environment not found at %VIRTUAL_ENV%
    exit /b 1
)

REM 保存原始 PATH
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

REM 将虚拟环境的 Scripts 目录添加到 PATH 最前面
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"

REM 设置提示符
if not defined _OLD_VIRTUAL_PROMPT set _OLD_VIRTUAL_PROMPT=%PROMPT%
set "PROMPT=(venv) %PROMPT%"

REM 清除 PYTHONHOME（如果存在）
if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

echo Virtual environment activated!
echo.
echo Virtual Env: %VIRTUAL_ENV%
echo Python: %VIRTUAL_ENV%\Scripts\python.exe
echo.
echo To install dependencies, run:
echo   pip install -r requirements.txt
echo   OR: python -m pip install -r requirements.txt
echo.
echo To run the ingest script, run:
echo   python ingest.py
echo.
echo To deactivate, run:
echo   deactivate
echo.

REM 保持环境变量在批处理文件结束后仍然有效
endlocal & (
    set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
    set "PROMPT=(venv) %PROMPT%"
    if defined PYTHONHOME set "PYTHONHOME="
)