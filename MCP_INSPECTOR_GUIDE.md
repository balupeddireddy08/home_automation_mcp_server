# MCP Inspector Testing Guide

## 🔍 What is MCP Inspector?

The MCP Inspector is an interactive web-based tool that lets you:
- Test all MCP tools without Claude Desktop
- See real-time requests and responses
- Debug tool parameters and outputs
- Verify your MCP server is working correctly

---

## 🚀 How to Run the Inspector

### Option 1: Using the Script (Easiest)

```powershell
# PowerShell
.\run_mcp_inspector.bat
# or
.\run_mcp_inspector.ps1
```

### Option 2: Direct Command

```powershell
python -m mcp.cli dev app/mcp_server_stdio.py
```

### What Happens:

The inspector will:
1. Start the MCP server
2. Launch a web interface at `http://localhost:6274`
3. Automatically open your browser
4. Show all available tools

---

## 🎯 Testing Your Tools

Once the inspector is open, you'll see all 9 tools:

### 1. **control_device**
Test controlling a light:
```json
{
  "action": "on",
  "room": "living_room",
  "device_type": "light",
  "brightness": 75
}
```

### 2. **get_device_status**
Get all devices:
```json
{}
```

Get bedroom devices:
```json
{
  "room": "bedroom"
}
```

### 3. **get_sensor_reading**
Get temperatures:
```json
{
  "sensor_type": "temperature"
}
```

### 4. **set_home_mode**
Set sleep mode:
```json
{
  "mode": "sleep"
}
```

### 5. **get_home_mode**
Check current mode:
```json
{}
```

### 6. **feed_fish**
Trigger fish feeder:
```json
{}
```

### 7. **water_plants**
Water front yard:
```json
{
  "zone": "front_yard",
  "duration": 10
}
```

### 8. **start_ev_charging**
Start charging:
```json
{}
```

### 9. **stop_ev_charging**
Stop charging:
```json
{}
```

---

## 🧪 Test Scenarios

### Scenario 1: Morning Routine

1. **Get status** - `get_device_status()`
2. **Set mode** - `set_home_mode(mode="home")`
3. **Turn on lights** - `control_device(action="on", room="kitchen", device_type="light")`
4. **Check temp** - `get_sensor_reading(sensor_type="temperature", room="bedroom")`

### Scenario 2: Leaving Home

1. **Set away mode** - `set_home_mode(mode="away")`
2. **Check locks** - `get_device_status(device_type="lock")`
3. **Verify lights off** - `get_device_status(device_type="light")`

### Scenario 3: Bedtime

1. **Set sleep mode** - `set_home_mode(mode="sleep")`
2. **Check bedroom** - `get_device_status(room="bedroom")`
3. **Verify locks** - `get_device_status(device_type="lock")`

---

## 📊 What to Look For

### ✅ Success Indicators:

1. **Server Starts**
   ```
   MCP Server: Database connected
   Starting MCP inspector...
   ```

2. **All 9 Tools Listed**
   - control_device
   - get_device_status
   - get_sensor_reading
   - set_home_mode
   - get_home_mode
   - feed_fish
   - water_plants
   - start_ev_charging
   - stop_ev_charging

3. **Tool Execution**
   - Returns formatted text responses
   - Updates database
   - Shows device changes

4. **Database State**
   - Devices persist between calls
   - State changes are saved
   - Events are logged

---

## 🔍 Inspector Features

### Tool Panel (Left)
- List of all available tools
- Click to expand and see parameters
- Input JSON for parameters

### Request Panel (Middle)
- Shows the exact MCP request
- JSON format
- Can copy for debugging

### Response Panel (Right)
- Tool execution results
- Formatted output
- Error messages if any

### Connection Status (Top)
- Server status indicator
- Reconnect button
- Session information

---

## 💡 Pro Tips

1. **Test Basic Tools First**
   - Start with `get_device_status()` to verify database
   - Then try `control_device()` to change states
   - Finally test complex `set_home_mode()`

2. **Watch for Database Changes**
   - After each tool call, run `get_device_status()` again
   - Verify that changes persisted

3. **Test Error Handling**
   - Try invalid device IDs
   - Use wrong parameter types
   - Check error messages are helpful

4. **Performance Testing**
   - Multiple rapid calls
   - Large queries (all devices)
   - Complex mode changes

---

## 🐛 Troubleshooting

### Inspector Won't Start

**Problem:** `ModuleNotFoundError: No module named 'mcp.cli'`

**Solution:**
```powershell
pip install "mcp[cli]"
```

### Database Errors

**Problem:** `Database file not found`

**Solution:**
```powershell
# Start API server first to create database
.\start_api_server.bat
# Then stop it (Ctrl+C) and run inspector
.\run_mcp_inspector.bat
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Already fixed in the code with `sys.path` adjustments. Make sure you're running from project root.

### Browser Doesn't Open

**Problem:** Inspector starts but browser doesn't open

**Solution:** Manually open the URL shown in the terminal:
```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...
```

---

## 🎓 After Testing

Once you verify everything works in the inspector:

1. **Configure Claude Desktop**
   ```powershell
   python app/stdio_config.py
   ```

2. **Add config to Claude Desktop** (see output from above command)

3. **Restart Claude Desktop**

4. **Test in Claude**
   ```
   "What's the status of my home?"
   "Turn on the living room lights"
   ```

---

## 📸 Expected Output

### Successful Tool Call:

```
✅ living_room_light_main: off → on (brightness: 100%)
✅ living_room_light_accent: off → on (brightness: 100%)
```

### Status Query:

```
📍 Living Room:
  💡 Living Room Light Main: ON [100%]
  💡 Living Room Light Accent: ON [100%]
  🌡️ Living Room Temp: ACTIVE [72°F]
  ...
```

### Mode Change:

```
🏠 Home mode set to: SLEEP

Actions taken:
💡 living_room_light_main: OFF
💡 bedroom_light: DIM (20%)
🔒 front_door_lock: LOCKED
🌡️ Thermostat: 68°F
```

---

## ✅ Verification Checklist

- [ ] Inspector starts without errors
- [ ] All 9 tools are listed
- [ ] `get_device_status()` returns 24 devices
- [ ] `control_device()` changes device state
- [ ] `set_home_mode()` executes multiple actions
- [ ] `get_sensor_reading()` returns temperatures
- [ ] `feed_fish()` updates fish feeder
- [ ] `water_plants()` starts sprinklers
- [ ] EV charging tools work
- [ ] Database persists changes

---

🎉 **Happy Testing!**

The MCP Inspector is a powerful tool for developing and debugging your MCP server before integrating with Claude Desktop.

