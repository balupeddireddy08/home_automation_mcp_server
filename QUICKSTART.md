# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend API Server

**Windows:**
```bash
start_api_server.bat
```

**macOS/Linux:**
```bash
chmod +x start_api_server.sh
./start_api_server.sh
```

**Or manually:**
```bash
cd app
python main.py
```

You should see:
```
Starting home automation server...
Database initialized at: C:\path\to\home_automation.db
Successfully seeded 24 devices.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Start the Frontend Dashboard

**Windows:**
```bash
start_frontend.bat
```

**macOS/Linux:**
```bash
chmod +x start_frontend.sh
./start_frontend.sh
```

**Or manually:**
```bash
cd frontend
npm install  # First time only
npm run dev
```

Open browser to: `http://localhost:5173`

You should see the Smart Home Dashboard with all devices!

### Step 4: Connect AI Assistant (Claude Desktop)

1. **Get MCP Configuration:**
   ```bash
   python app/stdio_config.py
   ```

2. **Copy the output** and add to Claude Desktop config:
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

3. **Restart Claude Desktop**

4. **Test in Claude:**
   ```
   "What's the status of my home?"
   "Turn on the living room lights"
   "Set bedroom temperature to 72"
   "I'm going to bed"
   ```

## ✅ Verification Steps

### Test API (in a new terminal)

```bash
# Check API is running
curl http://localhost:8000

# Get all devices
curl http://localhost:8000/api/devices

# Get statistics
curl http://localhost:8000/api/stats
```

### Test MCP Server Directly

```bash
python app/mcp_server_stdio.py
```

The server should start and wait for stdio input. Press `Ctrl+C` to exit.

### Test Frontend WebSocket

1. Open browser to `http://localhost:5173`
2. Open browser console (F12)
3. Check for WebSocket connection: `Connected` should show in header
4. Modify database directly to test real-time updates (optional)

## 🎯 Try These Commands in Claude Desktop

Once configured, try these natural language commands:

### Device Control
- "Turn on all lights in the living room"
- "Set the living room lights to 50% brightness"
- "Close all the blinds"
- "Lock all doors"
- "Open the garage door"

### Temperature Control
- "What's the temperature in the bedroom?"
- "Set the thermostat to 72 degrees"
- "What's the current temperature setting?"

### Status Queries
- "Show me the status of all devices"
- "What lights are currently on?"
- "Are all the doors locked?"
- "What's the status of the garage?"

### Home Modes
- "Set home mode to away" (when leaving)
- "I'm going to bed" (triggers sleep mode)
- "Good morning, prepare my home" (triggers home mode)
- "We're going on vacation" (triggers vacation mode)

### Special Actions
- "Feed the fish"
- "Water the front yard for 10 minutes"
- "Start charging my car"
- "Stop charging the car"

## 🔧 Troubleshooting

### API Server Won't Start
- **Error: Port 8000 in use**
  - Kill the process using port 8000 or change `API_PORT` in `app/config.py`
  
- **Module not found errors**
  - Run: `pip install -r requirements.txt`

### Frontend Not Loading
- **CORS errors**
  - Check that API server is running on port 8000
  - Verify CORS origins in `app/config.py`

- **WebSocket disconnected**
  - Ensure API server is running
  - Check browser console for errors

### MCP Server Not Working in Claude
- **Tools not appearing**
  - Verify config file path is correct
  - Check that Python path is correct in config
  - Restart Claude Desktop
  
- **Database locked**
  - Ensure only one MCP server instance is running
  - Close and reopen Claude Desktop

### Database Issues
- **Want to reset database?**
  ```bash
  # Delete the database file
  rm home_automation.db  # Linux/Mac
  del home_automation.db  # Windows
  
  # Restart API server to recreate
  python app/main.py
  ```

## 📊 Expected Behavior

### On First Run
1. API creates `home_automation.db` SQLite database
2. Initializes schema (4 tables)
3. Seeds 24 sample devices
4. Starts on port 8000

### Frontend Behavior
- Displays all 24 devices organized by room
- Shows real-time status (lights on/off, temperature, etc.)
- WebSocket connection indicator in header
- Statistics in sidebar (lights, locks, mode)

### MCP Server Behavior
- Connects via stdio (no visible output unless used with inspector)
- Provides 9 tools to AI assistant
- Updates database immediately
- Signals frontend via WebSocket manager

## 🎉 Success!

You should now have:
- ✅ API server running on http://localhost:8000
- ✅ Frontend dashboard on http://localhost:5173
- ✅ MCP server configured in Claude Desktop
- ✅ Real-time updates working
- ✅ AI assistant can control your smart home!

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [project structure](README.md#-project-structure)
- Try all the [example interactions](README.md#-example-ai-interactions)
- Customize device types and add your own tools

## 🆘 Still Having Issues?

1. Check that Python 3.10+ is installed: `python --version`
2. Check that Node.js is installed: `node --version`
3. Verify all dependencies are installed: `pip list`
4. Check the terminal output for error messages
5. Review the troubleshooting section above

Enjoy your AI-powered smart home! 🏠🤖

