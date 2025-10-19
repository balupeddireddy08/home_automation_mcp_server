#!/usr/bin/env pwsh
# PowerShell script to run MCP Inspector

Write-Host "Starting MCP Inspector for Home Automation Server..." -ForegroundColor Green
Write-Host ""
Write-Host "This will open the MCP Inspector in your browser." -ForegroundColor Cyan
Write-Host "You can test all 9 MCP tools interactively." -ForegroundColor Cyan
Write-Host ""

python -m mcp.cli dev app/mcp_server_stdio.py

