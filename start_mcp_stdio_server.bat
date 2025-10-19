@echo off
echo ========================================
echo Starting Home Automation MCP Server
echo ========================================
echo.
echo MCP Server Mode: stdio (for AI assistants)
echo.
echo This server provides 9 MCP tools:
echo   1. control_device
echo   2. get_device_status
echo   3. get_sensor_reading
echo   4. set_home_mode
echo   5. get_home_mode
echo   6. feed_fish
echo   7. water_plants
echo   8. start_ev_charging
echo   9. stop_ev_charging
echo.
echo Server is ready for AI assistant connections.
echo Press Ctrl+C to stop the server.
echo.
echo ========================================
python app/mcp_server_stdio.py

