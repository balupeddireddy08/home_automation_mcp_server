#!/usr/bin/env pwsh
# PowerShell script to start the React Frontend

Write-Host "Starting React Frontend..." -ForegroundColor Green
Write-Host "Frontend will be available at http://localhost:5173" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path (Join-Path $PSScriptRoot "frontend")
npm run dev

