@echo off
echo ========================================
echo Home Automation MCP Server - Testing
echo ========================================
echo.
echo Option 1: Test tools directly (Python)
echo Option 2: Run MCP server for Claude Desktop
echo.
echo Choose an option:
echo 1 - Test all tools with direct Python calls
echo 2 - Run MCP server (stdio) for Claude Desktop
echo 3 - Exit
echo.
choice /C 123 /N /M "Enter choice (1, 2, or 3): "

if errorlevel 3 goto :eof
if errorlevel 2 goto run_server
if errorlevel 1 goto test_tools

:test_tools
echo.
echo Testing all MCP tools...
echo.
python test_mcp_tools.py
pause
goto :eof

:run_server
echo.
echo Starting MCP server...
echo Press Ctrl+C to stop
echo.
python app/mcp_server_stdio.py
pause
goto :eof
