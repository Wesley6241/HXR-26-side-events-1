@echo off
REM 启动本地 HTTP 服务器来测试 HTML 页面
echo Starting local HTTP server...
echo.
echo Server will be available at: http://localhost:8000
echo Open http://localhost:8000/test.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM 使用 Python 的 HTTP 服务器
python -m http.server 8000
