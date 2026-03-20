@echo off
REM =========================
REM 一键启动 Node.js + ngrok
REM =========================

REM 切换到当前脚本所在目录
cd /d %~dp0

REM 启动 Node.js 服务器
echo 正在启动 Node.js 服务器...
start "" cmd /k "node server.js"

REM 等待 3 秒，确保服务器启动
timeout /t 3 /nobreak >nul

REM 启动 ngrok，暴露端口 3000
echo 正在启动 ngrok...
REM 如果 ngrok 不在环境变量，请写全路径，如 "C:\tools\ngrok.exe"
start "" cmd /k "ngrok http 3000"

REM 等待 1 秒，让 ngrok 启动
timeout /t 1 /nobreak >nul

REM 打印提示信息
echo.
echo ================================
echo Node.js 已启动，ngrok 已运行
echo 请查看 ngrok 窗口获取公网链接
echo ================================
pause
