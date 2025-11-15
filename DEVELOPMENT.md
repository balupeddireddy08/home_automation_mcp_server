# Development Guide

This guide covers development, testing, and technical implementation details for the Home Automation MCP Server.

## Table of Contents

- [Real-Time Updates Architecture](#real-time-updates-architecture)
- [Testing with MCP Inspector](#testing-with-mcp-inspector)
- [Database Schema](#database-schema)
- [Implementation Details](#implementation-details)
- [Performance Optimization](#performance-optimization)

## Real-Time Updates Architecture

### How MCP Changes Instantly Update the Frontend

The system uses database timestamp polling to detect changes and broadcast updates to connected clients.

```
┌─────────────────────┐
│  Claude Desktop     │  "Turn on the living room lights"
│  (AI Assistant)     │
└──────────┬──────────┘
           │ stdio MCP Protocol
           ↓
┌─────────────────────┐
│  FastMCP Server     │  1. Executes control_device()
│  (MCP Tools)        │  2. Updates database
└──────────┬──────────┘  3. Sets timestamp
           │
           ↓ SQL UPDATE
┌─────────────────────┐
│  SQLite Database    │  last_updated = NOW()
│  (Shared State)     │
└──────────┬──────────┘
           │
           ↓ Polls every 100ms
┌─────────────────────┐
│  FastAPI Server     │  4. Detects timestamp change
│  (Backend + WS)     │  5. Broadcasts to WebSocket
└──────────┬──────────┘
           │ WebSocket
           ↓ {type: "full_refresh"}
┌─────────────────────┐
│  React Frontend     │  6. Receives message
│  (Dashboard)        │  7. Fetches /api/devices
└─────────────────────┘  8. Re-renders UI
```

### Implementation Steps

**Step 1: MCP Tool Execution**

```python
# app/mcp_server_stdio.py
@mcp.tool()
async def control_device(action: str, device_id: str, brightness: int):
    await db.update_device(
        device_id,
        state="on",
        properties={"brightness": brightness}
    )
```

**Step 2: Database Update with Timestamp**

```python
# app/db/database.py
async def update_device(self, device_id: str, state: str, properties: dict):
    updates.append("last_updated = ?")
    params.append(datetime.now().isoformat())
    
    query = f"UPDATE devices SET {', '.join(updates)} WHERE id = ?"
    await self._connection.execute(query, params)
    await self._connection.commit()
```

**Step 3: FastAPI Polling Detection**

```python
# app/main.py
async def poll_database_changes():
    while True:
        await asyncio.sleep(0.1)  # Check every 100ms
        
        async with db._connection.execute(
            "SELECT MAX(last_updated) as max_time FROM devices"
        ) as cursor:
            current_update_time = (await cursor.fetchone())[0]
        
        if current_update_time != last_update_time:
            await ws_manager.broadcast_full_refresh()
            last_update_time = current_update_time
```

**Step 4: WebSocket Broadcast**

```python
# app/utils/websocket_manager.py
async def broadcast_full_refresh(self):
    message = {
        "type": "full_refresh",
        "timestamp": datetime.now().isoformat()
    }
    for connection in self.active_connections:
        await connection.send_json(message)
```

**Step 5: Frontend Receives Update**

```javascript
// frontend/src/App.jsx
useEffect(() => {
  if (lastMessage) {
    handleRealtimeUpdate(lastMessage)
  }
}, [lastMessage])

const handleRealtimeUpdate = (update) => {
  if (update.type === 'full_refresh') {
    fetchDevices()
    fetchStats()
  }
}
```

### Performance Metrics

| Step | Action | Time |
|------|--------|------|
| 1 | MCP tool executes | < 50ms |
| 2 | Database update | < 10ms |
| 3 | Polling detects change | < 100ms |
| 4 | WebSocket broadcast | < 20ms |
| 5 | Frontend receives | < 10ms |
| 6 | API fetch + render | < 100ms |
| **Total** | **End-to-end latency** | **< 300ms** |

### Why This Architecture?

**Advantages:**
- ✅ Simple - No complex message queues
- ✅ Reliable - Database is source of truth
- ✅ Fast - 100ms polling is imperceptible
- ✅ Scalable - Works with multiple clients
- ✅ Process-Independent - MCP and API servers don't need direct communication

**Configuration:**

```python
# app/config.py
UPDATE_CHECK_INTERVAL = 0.1  # 100ms (default)
# Faster: 0.05 (50ms) - higher CPU, faster updates
# Slower: 0.2 (200ms) - lower CPU, still fast enough
```

## Testing with MCP Inspector

The MCP Inspector is a web-based tool for testing MCP tools interactively.

### Starting the Inspector

```bash
npx @modelcontextprotocol/inspector python app/mcp_server_stdio.py
```

The inspector opens at `http://localhost:6274`

### Test Scenarios

**Scenario 1: Morning Routine**
1. `get_device_status()` - Check all devices
2. `set_home_mode(mode="home")` - Set home mode
3. `control_device(action="on", room="kitchen", device_type="light")` - Turn on kitchen lights
4. `get_sensor_reading(sensor_type="temperature", room="bedroom")` - Check temperature

**Scenario 2: Leaving Home**
1. `set_home_mode(mode="away")` - Set away mode
2. `get_device_status(device_type="lock")` - Verify locks
3. `get_device_status(device_type="light")` - Verify lights off

**Scenario 3: Bedtime**
1. `set_home_mode(mode="sleep")` - Set sleep mode
2. `get_device_status(room="bedroom")` - Check bedroom devices
3. `get_device_status(device_type="lock")` - Verify locks

### Inspector Features

- **Tool Panel (Left)** - List of available tools with parameter inputs
- **Request Panel (Middle)** - Shows MCP request JSON
- **Response Panel (Right)** - Tool execution results
- **Connection Status (Top)** - Server connection indicator

### Example Tool Tests

**Control Device:**
```json
{
  "action": "on",
  "room": "living_room",
  "device_type": "light",
  "brightness": 75
}
```

**Get Sensor Reading:**
```json
{
  "sensor_type": "temperature",
  "room": "bedroom"
}
```

**Set Home Mode:**
```json
{
  "mode": "sleep"
}
```

**Water Plants:**
```json
{
  "zone": "front_yard",
  "duration": 10
}
```

## Database Schema

### Tables

**devices**
```sql
CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    room TEXT NOT NULL,
    state TEXT NOT NULL,
    properties TEXT,  -- JSON
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_devices_room ON devices(room);
CREATE INDEX idx_devices_type ON devices(type);
CREATE INDEX idx_devices_last_updated ON devices(last_updated);
```

**events**
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    device_id TEXT,
    action TEXT,
    metadata TEXT,  -- JSON
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_events_timestamp ON events(timestamp);
```

**home_modes**
```sql
CREATE TABLE home_modes (
    mode TEXT PRIMARY KEY,
    is_active BOOLEAN DEFAULT 0,
    last_activated TIMESTAMP
);
```

**automations**
```sql
CREATE TABLE automations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    conditions TEXT,  -- JSON
    actions TEXT,     -- JSON
    enabled BOOLEAN DEFAULT 1
);
```

### Database Operations

**Create/Seed Database:**
```bash
# Database is automatically created on first run
python app/main.py
```

**Reset Database:**
```bash
# Delete database file
rm home_automation.db  # Linux/Mac
del home_automation.db  # Windows

# Restart API server to recreate
python app/main.py
```

**Query Database Directly:**
```bash
sqlite3 home_automation.db "SELECT * FROM devices;"
sqlite3 home_automation.db "SELECT MAX(last_updated) FROM devices;"
sqlite3 home_automation.db "SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;"
```

## Implementation Details

### Device Types and Properties

```python
# app/models/device.py
DEVICE_TYPES = {
    "light": {"brightness": int, "color_temp": int},
    "fan": {"speed": int},
    "blinds": {"position": int},
    "thermostat": {"target_temp": float, "current_temp": float, "mode": str},
    "lock": {},
    "garage": {},
    "temperature_sensor": {"value": float, "unit": str},
    "motion_sensor": {"motion_detected": bool, "last_motion": str},
    "sprinkler": {"zone": str, "duration": int},
    "ev_charger": {"battery_level": int, "charging": bool},
    "fish_feeder": {"last_fed": str}
}
```

### MCP Tool Implementation Pattern

```python
# app/mcp_server_stdio.py
@mcp.tool()
async def tool_name(
    param1: str,
    param2: int = None,
    ctx: Context = None
) -> str:
    """
    Tool description for AI assistant.
    
    Args:
        param1: First parameter
        param2: Optional second parameter
    
    Returns:
        Human-readable result string
    """
    # 1. Validate inputs
    if not param1:
        raise ValueError("param1 is required")
    
    # 2. Perform operation (update database)
    await db.operation(param1, param2)
    
    # 3. Log progress (optional)
    if ctx:
        await ctx.info(f"Processing {param1}")
    
    # 4. Return formatted result
    return f"✅ Operation completed: {param1}"
```

### WebSocket Manager

```python
# app/utils/websocket_manager.py
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                await self.disconnect(connection)
```

### Home Mode Execution

```python
# app/mcp_server_stdio.py
HOME_MODES = {
    "home": {
        "lights": {"living_room": {"state": "on", "brightness": 75}},
        "thermostat": {"target_temp": 72, "mode": "auto"}
    },
    "away": {
        "lights": {"*": {"state": "off"}},
        "locks": {"*": {"state": "locked"}},
        "thermostat": {"target_temp": 65, "mode": "eco"}
    },
    "sleep": {
        "lights": {
            "bedroom": {"state": "on", "brightness": 20},
            "*": {"state": "off"}
        },
        "locks": {"*": {"state": "locked"}},
        "thermostat": {"target_temp": 68}
    },
    "vacation": {
        "lights": {"*": {"state": "off"}},
        "locks": {"*": {"state": "locked"}},
        "thermostat": {"target_temp": 60, "mode": "eco"}
    }
}
```

## Performance Optimization

### Database Optimization

1. **WAL Mode** (Write-Ahead Logging)
```python
# Automatically enabled in database.py
await self._connection.execute("PRAGMA journal_mode=WAL")
```

2. **Indexes**
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_devices_room ON devices(room);
CREATE INDEX idx_devices_type ON devices(type);
CREATE INDEX idx_devices_last_updated ON devices(last_updated);
```

3. **Connection Pooling**
```python
# Use single connection with WAL mode for concurrent reads
# app/db/database.py handles this automatically
```

### WebSocket Optimization

1. **Connection Management**
```python
# Track and clean up stale connections
async def cleanup_stale_connections(self):
    for conn in self.active_connections:
        if not await conn.is_alive():
            self.disconnect(conn)
```

2. **Message Batching**
```python
# Batch multiple rapid changes
async def broadcast_with_debounce(self, delay=0.1):
    if not self._pending_broadcast:
        self._pending_broadcast = True
        await asyncio.sleep(delay)
        await self.broadcast_full_refresh()
        self._pending_broadcast = False
```

### Polling Optimization

1. **Efficient Timestamp Query**
```sql
-- Use MAX() instead of scanning all rows
SELECT MAX(last_updated) as max_time FROM devices;
```

2. **Conditional Broadcasting**
```python
# Only broadcast when timestamp actually changed
if current_update_time != last_update_time:
    await ws_manager.broadcast_full_refresh()
```

### Frontend Optimization

1. **React Memoization**
```javascript
// Memoize device cards to prevent unnecessary re-renders
const DeviceCard = React.memo(({ device }) => {
  // Component code
});
```

2. **WebSocket Reconnection**
```javascript
// Automatically reconnect on disconnect
const { lastMessage, readyState } = useWebSocket(url, {
  shouldReconnect: () => true,
  reconnectInterval: 3000
});
```

## Production Considerations

### For Large-Scale Deployments

1. **Use Redis Pub/Sub** for multi-server deployments
2. **Add database replication** for read scaling
3. **Implement WebSocket load balancing** with sticky sessions
4. **Add change coalescing** to batch multiple rapid changes
5. **Monitor polling overhead** (should be < 1% CPU)
6. **Add health check endpoints** for monitoring
7. **Implement rate limiting** on API endpoints
8. **Add authentication** for production use

### Monitoring

```python
# Add metrics collection
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Log metrics
    return response
```

### Logging

```python
# app/config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Development Workflow

### Local Development

```bash
# Terminal 1: API Server with auto-reload
uvicorn app.main:app --reload

# Terminal 2: Frontend with hot reload
cd frontend && npm run dev

# Terminal 3: Test MCP tools
python app/mcp_server_stdio.py
```

### Testing Workflow

```bash
# 1. Test installation
python test_installation.py

# 2. Test MCP tools directly
python test_mcp_tools.py

# 3. Test with Inspector
npx @modelcontextprotocol/inspector python app/mcp_server_stdio.py

# 4. Test real-time updates
python test_realtime_updates.py
```

### Code Quality

```bash
# Format code
black app/
isort app/

# Type checking
mypy app/

# Linting
pylint app/
ruff check app/
```

## Additional Resources

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [SQLite Performance Tips](https://www.sqlite.org/performance.html)
- [WebSocket Guide](https://websockets.readthedocs.io/)

