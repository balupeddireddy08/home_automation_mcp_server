@echo off
echo ========================================
echo  Home Automation System Launcher
echo ========================================
echo.
echo Select what to start:
echo.
echo  1. API Server (Backend + WebSocket)
echo  2. Frontend (React Dashboard)
echo  3. MCP Server (For Claude Desktop)
echo  4. MCP Inspector (Testing Tool)
echo.
echo  0. Exit
echo.
echo ========================================

set /p choice=Enter your choice (0-4): 

if "%choice%"=="1" (
    echo.
    echo Starting API Server at http://localhost:8000
    echo Press Ctrl+C to stop
    echo.
    python app/main.py
)

if "%choice%"=="2" (
    echo.
    echo Starting Frontend at http://localhost:5173
    echo Press Ctrl+C to stop
    echo.
    cd frontend
    npm run dev
)

if "%choice%"=="3" (
    echo.
    echo Starting MCP Server (stdio mode)
    echo This runs in the background for Claude Desktop
    echo Press Ctrl+C to stop
    echo.
    python app/mcp_server_stdio.py
)

if "%choice%"=="4" (
    echo.
    echo Starting MCP Inspector at http://localhost:6274
    echo Browser will open automatically
    echo Press Ctrl+C to stop
    echo.
    npx @modelcontextprotocol/inspector python app/mcp_server_stdio.py
)

if "%choice%"=="0" (
    echo.
    echo Exiting...
    exit
)

echo.
echo Invalid choice. Please run the script again.
pause

