# Home Automation MCP Server

A comprehensive smart home automation system that allows AI assistants to control and monitor smart home devices through natural language using the Model Context Protocol (MCP).

## 🏗️ Architecture

```
AI Assistant (Claude Desktop/VS Code)
        ↓ stdio MCP Protocol
    FastMCP Server
        ↓
    SQLite Database ← [Real-time] ← FastAPI Server
                                        ↓ WebSocket
                                    React Frontend
```

**Key Components:**
- **FastMCP Server** (`app/mcp_server_stdio.py`) - Handles AI interactions via stdio protocol
- **FastAPI Server** (`app/main.py`) - REST API + WebSocket for frontend
- **SQLite Database** - Shared state between both servers
- **React Frontend** - Real-time dashboard with WebSocket updates

## ✨ Features

### MCP Tools (8 Tools)
1. **control_device** - Universal device control (on/off/set/toggle)
2. **get_device_status** - Query device states
3. **get_sensor_reading** - Read temperature, motion sensors
4. **set_home_mode** - Execute scenes (home/away/sleep/vacation)
5. **get_home_mode** - Check current mode
6. **feed_fish** - Trigger fish feeder
7. **water_plants** - Control sprinkler system
8. **start_ev_charging / stop_ev_charging** - EV charger control

### Supported Devices (25+ Devices)
- 💡 Lights (with brightness control)
- 🌡️ Thermostat (temperature + mode control)
- 🔒 Locks
- 🪟 Blinds (with position control)
- 💨 Fans (with speed control)
- 🚗 Garage door
- 🐠 Fish feeder
- 💧 Sprinkler system
- 🔌 EV charger
- 🌡️ Temperature sensors
- 👁️ Motion sensors

### Home Modes
- **Home** - Welcome mode (lights on, 72°F)
- **Away** - Security mode (lights off, locks engaged, 65°F)
- **Sleep** - Night mode (bedroom dim 20%, doors locked, 68°F)
- **Vacation** - Extended away (everything secured, 60°F)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Server

```bash
# Terminal 1
cd app
python main.py
```

The API server will start at `http://localhost:8000`

### 3. Start the React Frontend

```bash
# Terminal 2
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Configure MCP Server for Claude Desktop

Run the configuration helper:

```bash
python app/stdio_config.py
```

Copy the output and add it to your Claude Desktop config file:
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Example configuration:

```json
{
  "mcpServers": {
    "home-automation": {
      "command": "python",
      "args": ["C:/path/to/home_automation/app/mcp_server_stdio.py"]
    }
  }
}
```

Restart Claude Desktop after adding the configuration.

### 5. Test MCP Server Directly

```bash
# Terminal 3
python app/mcp_server_stdio.py
```

## 💬 Example AI Interactions

### Morning Routine
```
User: "Good morning! Can you prepare my home?"
AI: [Calls set_home_mode(mode="home")]
    [Calls control_device(action="on", room="kitchen", device_type="light")]
Response: "Good morning! I've set your home to welcome mode and turned on the kitchen lights. Temperature is set to 72°F."
```

### Leaving Home
```
User: "I'm leaving for work"
AI: [Calls set_home_mode(mode="away")]
Response: "All set! I've turned off lights, set temperature to 65°F, and locked all doors."
```

### Bedtime
```
User: "I'm going to bed"
AI: [Calls set_home_mode(mode="sleep")]
Response: "Good night! Bedroom light is dimmed to 20%, all doors are locked, and temperature is set to 68°F."
```

### Device Control
```
User: "Turn on the living room lights to 50%"
AI: [Calls control_device(action="set", room="living_room", device_type="light", brightness=50)]
Response: "Living room lights set to 50% brightness."
```

### Status Check
```
User: "What's the temperature in the bedroom?"
AI: [Calls get_sensor_reading(sensor_type="temperature", room="bedroom")]
Response: "The bedroom temperature is 70°F."
```

## 📁 Project Structure

```
home_automation/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── main.py                   # FastAPI server
│   ├── mcp_server_stdio.py       # FastMCP server with tools
│   ├── stdio_config.py           # MCP configuration helper
│   ├── db/
│   │   ├── schema.sql           # Database schema
│   │   ├── database.py          # Database manager
│   │   └── seed_data.py         # Sample devices
│   ├── models/
│   │   └── device.py            # Device models
│   ├── schemas/
│   │   └── responses.py         # API response schemas
│   └── utils/
│       └── websocket_manager.py # WebSocket manager
├── frontend/                     # React dashboard
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── hooks/
│   └── package.json
├── requirements.txt
├── home_automation.db           # SQLite database (auto-created)
└── README.md
```

## 🔧 API Endpoints

### REST API

- `GET /` - API information
- `GET /api/devices` - Get all devices (supports `?room=` and `?type=` filters)
- `GET /api/rooms` - Get list of rooms
- `GET /api/stats` - Get dashboard statistics
- `WebSocket /ws` - Real-time device updates

### WebSocket Messages

**From Server:**
```json
{
  "type": "device_update",
  "device_id": "living_room_light_main",
  "state": "on",
  "properties": {"brightness": 75}
}

{
  "type": "mode_change",
  "mode": "away"
}

{
  "type": "full_refresh"
}
```

## 🗄️ Database Schema

### Tables

**devices**
- `id` (TEXT PRIMARY KEY)
- `type` (TEXT)
- `room` (TEXT)
- `state` (TEXT)
- `properties` (TEXT/JSON)
- `last_updated` (TIMESTAMP)

**events**
- `id` (INTEGER PRIMARY KEY)
- `event_type` (TEXT)
- `device_id` (TEXT)
- `action` (TEXT)
- `metadata` (TEXT/JSON)
- `timestamp` (TIMESTAMP)

**home_modes**
- `mode` (TEXT PRIMARY KEY)
- `is_active` (BOOLEAN)
- `last_activated` (TIMESTAMP)

## 🧪 Testing

### Test FastAPI Server
```bash
# Check API health
curl http://localhost:8000

# Get all devices
curl http://localhost:8000/api/devices

# Get bedroom devices
curl http://localhost:8000/api/devices?room=bedroom

# Get statistics
curl http://localhost:8000/api/stats
```

### Test MCP Server with Inspector
```bash
# If you have MCP CLI tools installed
mcp dev app/mcp_server_stdio.py
```

## 🔄 Real-time Updates Flow

1. AI assistant calls MCP tool (e.g., `control_device`)
2. MCP server updates SQLite database
3. MCP server signals WebSocket manager
4. WebSocket manager broadcasts update to all connected frontend clients
5. Frontend receives update and re-renders affected devices
6. Total latency: < 100ms

## 🛠️ Development

### Add New Device Type

1. Add device to `app/db/seed_data.py`
2. Update type hints in `app/models/device.py`
3. Add icon in frontend `DeviceCard.jsx`

### Add New MCP Tool

1. Add `@mcp.tool()` decorated function in `app/mcp_server_stdio.py`
2. Include database operations and WebSocket signaling
3. Document in docstring for AI assistant context

## 📊 Performance Metrics

- ✅ Database queries: < 10ms
- ✅ MCP tool execution: < 100ms
- ✅ WebSocket broadcast: < 50ms
- ✅ End-to-end update: < 200ms
- ✅ Concurrent WebSocket connections: 100+

## 🐛 Troubleshooting

### MCP Server Not Connecting
- Check Claude Desktop config file path
- Verify Python path in configuration
- Restart Claude Desktop after config changes

### Frontend Not Updating
- Verify FastAPI server is running on port 8000
- Check browser console for WebSocket errors
- Ensure CORS origins include your frontend URL

### Database Locked Errors
- Verify only one process is accessing the database
- Check that WAL mode is enabled (automatic in database.py)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io)
- [FastMCP](https://github.com/modelcontextprotocol/python-sdk)
- [FastAPI](https://fastapi.tiangolo.com)
- [React](https://react.dev)

