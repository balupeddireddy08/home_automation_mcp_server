#!/usr/bin/env pwsh
# PowerShell script to start the Home Automation API Server

Write-Host "Starting Home Automation FastAPI Server..." -ForegroundColor Green
Write-Host "Server will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

python app/main.py

