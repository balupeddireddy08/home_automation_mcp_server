# How to Run the Home Automation System

## ✅ Code Status: All Working!

Your code has been tested and all imports are working correctly. Here's how to run the system:

---

## 🚀 Running on Windows PowerShell

### Option 1: Use PowerShell Scripts (Recommended)

```powershell
# Start API Server
.\start_api_server.ps1

# Start Frontend (in another terminal)
.\start_frontend.ps1
```

### Option 2: Use Batch Files with PowerShell

In PowerShell, you need to use `.\` prefix:

```powershell
# Start API Server
.\start_api_server.bat

# Start Frontend (in another terminal)
.\start_frontend.bat
```

### Option 3: Direct Commands

```powershell
# Terminal 1: Start API Server
cd app
python main.py

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

---

## 🚀 Running on Command Prompt (cmd.exe)

If you're using Command Prompt instead of PowerShell:

```cmd
REM Start API Server
start_api_server.bat

REM Start Frontend (in another window)
start_frontend.bat
```

---

## 🚀 Running on Linux/Mac

```bash
# Make scripts executable (first time only)
chmod +x start_api_server.sh start_frontend.sh

# Start API Server
./start_api_server.sh

# Start Frontend (in another terminal)
./start_frontend.sh
```

---

## ✅ Verification

### 1. Check if API Server is Running

Open browser to: http://localhost:8000

You should see:
```json
{
  "message": "Home Automation API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### 2. Check if Frontend is Running

Open browser to: http://localhost:5173

You should see the Smart Home Dashboard with all devices.

### 3. Test API Endpoints

```powershell
# PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/api/devices" | Select-Object -Expand Content

# Or use curl (if installed)
curl http://localhost:8000/api/devices
```

---

## 🐛 Common Issues

### Issue: "Command not recognized" in PowerShell

**Solution**: Use `.\` prefix before the script name:
```powershell
.\start_api_server.bat
# NOT: start_api_server.bat
```

### Issue: "Cannot load script because running scripts is disabled"

**Solution**: Enable script execution (run PowerShell as Administrator):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:
```powershell
.\start_api_server.ps1
```

### Issue: "Port 8000 already in use"

**Solution**: Kill the existing process:
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Kill Python processes
Get-Process python | Stop-Process -Force
```

### Issue: Frontend shows "Disconnected"

**Solution**: Make sure API server is running first on port 8000, then start frontend.

---

## 📋 Full Startup Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install frontend deps: `cd frontend && npm install`
- [ ] Start API server (Terminal 1)
- [ ] Wait for "Uvicorn running on http://0.0.0.0:8000"
- [ ] Start frontend (Terminal 2)
- [ ] Open http://localhost:5173
- [ ] Check WebSocket shows "Connected"
- [ ] Test device control in dashboard

---

## 🎯 Quick Test Commands

### Test Installation
```powershell
python test_installation.py
```

Should output: `[SUCCESS] All tests passed!`

### Test API Server
```powershell
# Start server in background (PowerShell 7+)
Start-Process python -ArgumentList "app/main.py"

# Wait a moment, then test
Start-Sleep -Seconds 3
Invoke-WebRequest http://localhost:8000
```

### Test MCP Server
```powershell
python app/stdio_config.py
```

---

## 💡 Tips

1. **Use separate terminals** - One for API server, one for frontend
2. **API server first** - Always start the API server before the frontend
3. **Check ports** - Make sure ports 8000 and 5173 are available
4. **Watch for errors** - Look at terminal output for any error messages
5. **Restart if needed** - Press Ctrl+C to stop, then restart

---

## 🎉 Your Code is Working!

All tests passed:
- ✅ Python imports: OK
- ✅ FastAPI app: OK  
- ✅ MCP server: OK
- ✅ Database: OK
- ✅ All dependencies: Installed

The only issue was running the scripts in PowerShell (need `.\` prefix).

**You're ready to go! Start the servers and enjoy your AI-powered smart home!** 🏠🤖

