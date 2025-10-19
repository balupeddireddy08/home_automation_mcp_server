#!/usr/bin/env pwsh
# PowerShell script to start the Home Automation MCP Server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Home Automation MCP Server" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "MCP Server Mode: stdio (for AI assistants)" -ForegroundColor Yellow
Write-Host ""
Write-Host "This server provides 9 MCP tools:" -ForegroundColor White
Write-Host "  1. control_device" -ForegroundColor Gray
Write-Host "  2. get_device_status" -ForegroundColor Gray
Write-Host "  3. get_sensor_reading" -ForegroundColor Gray
Write-Host "  4. set_home_mode" -ForegroundColor Gray
Write-Host "  5. get_home_mode" -ForegroundColor Gray
Write-Host "  6. feed_fish" -ForegroundColor Gray
Write-Host "  7. water_plants" -ForegroundColor Gray
Write-Host "  8. start_ev_charging" -ForegroundColor Gray
Write-Host "  9. stop_ev_charging" -ForegroundColor Gray
Write-Host ""
Write-Host "Server is ready for AI assistant connections." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

python app/mcp_server_stdio.py

