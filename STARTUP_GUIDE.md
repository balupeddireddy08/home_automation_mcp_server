# Home Automation System - Startup Guide

## 🚀 All Startup Scripts

You now have **5 different ways** to start your home automation system components!

---

## 1️⃣ FastAPI Server (Backend + WebSocket)

**Purpose:** REST API + WebSocket for the React frontend

### Windows:
```powershell
.\start_api_server.bat
# or
.\start_api_server.ps1
```

### Direct Command:
```powershell
python app/main.py
```

**Runs on:** http://localhost:8000  
**Use for:** Frontend dashboard connectivity

---

## 2️⃣ React Frontend (Dashboard)

**Purpose:** Web dashboard with real-time device updates

### Windows:
```powershell
.\start_frontend.bat
# or
.\start_frontend.ps1
```

### Direct Command:
```powershell
cd frontend
npm run dev
```

**Runs on:** http://localhost:5173  
**Use for:** Visual device control and monitoring

---

## 3️⃣ MCP Server (AI Assistant)

**Purpose:** stdio server for Claude Desktop and other AI assistants

### Windows:
```powershell
.\start_mcp_stdio_server.bat
# or
.\start_mcp_stdio_server.ps1
```

### Direct Command:
```powershell
python app/mcp_server_stdio.py
```

**Protocol:** stdio (standard input/output)  
**Use for:** AI assistant integration (Claude Desktop)

---

## 4️⃣ MCP Inspector (Testing)

**Purpose:** Interactive web-based tool to test MCP tools

### Command:
```powershell
npx @modelcontextprotocol/inspector python app/mcp_server_stdio.py
```

**Runs on:** http://localhost:6274  
**Use for:** Testing and debugging MCP tools before production

---

## 5️⃣ Direct Tool Testing

**Purpose:** Test all 9 MCP tools with direct Python calls

### Windows:
```powershell
.\run_mcp_inspector.bat
# Choose option 1
```

### Direct Command:
```powershell
python test_mcp_tools.py
```

**Output:** Terminal-based test results  
**Use for:** Quick development testing

---

## 📋 Common Startup Sequences

### For Frontend Development:
```powershell
# Terminal 1: Start API server
.\start_api_server.bat

# Terminal 2: Start frontend
.\start_frontend.bat

# Open browser to http://localhost:5173
```

### For AI Assistant Setup:
```powershell
# Get Claude Desktop config
python app/stdio_config.py

# Add config to Claude Desktop
# Then the MCP server runs automatically when Claude starts
```

### For MCP Tool Testing:
```powershell
# Option A: Interactive inspector
npx @modelcontextprotocol/inspector python app/mcp_server_stdio.py

# Option B: Direct testing
python test_mcp_tools.py
```

### Full System Demo:
```powershell
# Terminal 1: API Server
.\start_api_server.bat

# Terminal 2: Frontend
.\start_frontend.bat

# Terminal 3: Test MCP tools
python test_mcp_tools.py

# Browser: http://localhost:5173 (watch real-time updates)
```

---

## 🔧 Port Reference

| Component | Port | URL |
|-----------|------|-----|
| FastAPI Server | 8000 | http://localhost:8000 |
| React Frontend | 5173 | http://localhost:5173 |
| MCP Inspector | 6274 | http://localhost:6274 |
| MCP Proxy | 6277 | (internal use) |
| MCP stdio Server | N/A | stdin/stdout |

---

## 🎯 Quick Command Reference

### Start Everything:
```powershell
# 3 terminals needed:

# Terminal 1 - Backend
.\start_api_server.bat

# Terminal 2 - Frontend  
.\start_frontend.bat

# Terminal 3 - Optional: Testing
python test_mcp_tools.py
```

### Stop Everything:
```powershell
# Press Ctrl+C in each terminal
# Or kill all processes:
Get-Process python,node | Stop-Process -Force
```

### Check What's Running:
```powershell
# Check ports
Get-NetTCPConnection -LocalPort 8000,5173,6274 -ErrorAction SilentlyContinue

# Check processes
Get-Process python,node -ErrorAction SilentlyContinue
```

---

## 📝 Script Descriptions

### `start_api_server.bat/.ps1`
- Starts FastAPI backend server
- Initializes SQLite database
- Seeds 24 sample devices
- Enables WebSocket for real-time updates

### `start_frontend.bat/.ps1`
- Starts React development server
- Opens at http://localhost:5173
- Connects to API server via WebSocket

### `start_mcp_stdio_server.bat/.ps1`
- Starts MCP server in stdio mode
- Waits for MCP protocol messages
- Used by Claude Desktop and AI assistants

### `run_mcp_inspector.bat`
- Interactive menu for testing options
- Runs direct tool tests or MCP server

### `test_mcp_tools.py`
- Direct Python testing of all 9 tools
- Shows formatted output
- No inspector needed

---

## 🆘 Troubleshooting

### Port Already in Use:
```powershell
# Kill process on specific port
Get-NetTCPConnection -LocalPort 8000 | 
  Select-Object -ExpandProperty OwningProcess | 
  ForEach-Object { Stop-Process -Id $_ -Force }
```

### MCP Inspector Won't Start:
```powershell
# Clear ports 6274 and 6277
Get-NetTCPConnection -LocalPort 6274,6277 -ErrorAction SilentlyContinue | 
  Select-Object -ExpandProperty OwningProcess | 
  ForEach-Object { Stop-Process -Id $_ -Force }

# Then restart
npx @modelcontextprotocol/inspector python app/mcp_server_stdio.py
```

### Python Module Errors:
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

### Database Issues:
```powershell
# Reset database
Remove-Item home_automation.db -ErrorAction SilentlyContinue
# Restart API server to recreate
.\start_api_server.bat
```

---

## ✅ Success Checklist

- [ ] FastAPI server starts on port 8000
- [ ] Frontend opens on port 5173
- [ ] WebSocket shows "Connected" in dashboard
- [ ] All 24 devices visible in frontend
- [ ] MCP tools tested successfully
- [ ] Claude Desktop configured (optional)

---

## 🎉 You're All Set!

Your home automation system has multiple ways to start and test:

1. **Development:** Use API server + Frontend
2. **Testing:** Use test_mcp_tools.py or Inspector
3. **Production:** Configure Claude Desktop with MCP server

All scripts are ready to use! 🏠🤖

